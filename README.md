# Snakemake-asm-evaluation-vg
Assessing assemblies with variation graphs.
> WIP

![](docs/chm13_simple_repeat.png)

## Workflow
1. Align all assemblies with minimap2
2. Query each region in provided bedfile with impg.
3. Generate variation graph of queried regions with minigraph.
4. Rename segments in rGFA to SN tag.
5. Visualize with Bandage.

## Usage
```bash
snakemake -np --configfile config.yaml 
```

## Test
On a simple repeat region flagged by NucFlag v1.0 from three CHM13 assemblies (`hifiasm v0.25.0`, `Verkko 2.2.1`, and `Verkko 2.3`).
* See `test/input/misassemblies.bed`

```bash
snakemake -np --configfile test/config/config.yaml
```

## TODO
* [ ] - Inject annotations into graph as *segments* not paths. Tried odgi inject but expects numerical segments so not suited for our use-case.
* [ ] - Call variation from graph and intersect with provided annotations.
