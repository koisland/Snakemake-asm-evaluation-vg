import sys
import argparse


def main():
    ap = argparse.ArgumentParser(description="Rename segments in GFAv1.1 or rGFA to SN tag.")
    ap.add_argument("infile", type=str, help="Input GFA v1.1 or rGFA file. All segments are expected to come first.")
    ap.add_argument("-o", "--outfile", type=str, default=None, help="Output GFA")
    args = ap.parse_args()

    infile: str = args.infile
    outfile: str | None = args.outfile
    with (
        (sys.stdin if infile == "-" else open(infile, "rt")) as fh ,
        (open(outfile, "wt") if outfile else sys.stdout) as ofh,
    ):
        # https://gfa-spec.github.io/GFA-spec/GFA1.html
        segments = {}
        for line in fh:
            line: str = line.strip()
            if line.startswith("S"):
                rtype, name, sequence, *tags = line.split("\t")
                for t in tags:
                    tname, tdtype, tvalue = t.split(":", 2)
                    if tname != "SN":
                        continue
                    segments[name] = f"{tvalue}_{name}"
                final_name = segments[name] if name in segments else name
                print(rtype, final_name, sequence, *tags, sep="\t", file=ofh)
            elif line.startswith("L"):
                rtype, frm, frm_ort, to, to_ort, ovl, *tags = line.split("\t")
                frm = segments.get(frm, frm)
                to = segments.get(to, to)
                print(rtype, frm, frm_ort, to, to_ort, ovl, *tags, sep="\t", file=ofh)
            elif line.startswith("C"):
                rtype, cont, cont_ort, contd, contd_ort, pos, ovl = line.split("\t")
                cont = segments.get(cont, cont)
                contd = segments.get(contd, contd)
                print(rtype, cont, cont_ort, contd, contd_ort, pos, ovl, sep="\t", file=ofh)
            elif line.startswith("P"):
                rtype, path_name, segm_names, ovl = line.split("\t")
                new_segm_names = []
                for segm_ort in segm_names.split(","):
                    segm = segm_ort[:-1]
                    ort = segm_ort[-1]
                    segm = segments.get(segm, segm)
                    assert "," not in segm, f"New segment name {segm} contains comma."
                    new_segm_names.append(f"{segm}{ort}")
                print(rtype, path_name, ",".join(new_segm_names), ovl, sep="\t", file=ofh)
            else:
                print(line, file=ofh)

if __name__ == "__main__":
    raise SystemExit(main())
