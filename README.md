# miniref: Minimalist Reference Management Using the Command Line
miniref is an experiment at creating an **academic reference manager** (in the sense of [Zotero](https://www.zotero.org)), but for the **command line** and with a **minimalist flavour**. It is strongly inspired by projects like [Cobib](https://mrossinek.gitlab.io/programming/introducing-cobib/) and [fast-p](https://github.com/bellecp/fast-p) (the latter which appears to originate the idea of using `fzf` for searching PDF literature). 

# Requirements
* Python 3
* [fzf](https://github.com/junegunn/fzf)
* Standard Unix/Linux shell utilities (originally developed under OpenBSD 7.3 against `sh`; strict compatibility not guaranteed).
* xpdf

# Installation
* Copy contents of `scripts/` to a location on your `$PATH` (e.g. `~/bin`. Redefine `PATH=$PATH:$HOME/bin` if necessary)
* Install [fzf](https://github.com/junegunn/fzf)
* `export REFS=/path/to/your/references`
* Add suggested aliases to your shell config (e.g. `.bashrc`), if desired
  
# Features
Consider the following bare directory structure for storing references:
```
references/
|-- all
|   `-- to_read   <---  Add new references here, move references to parent once read
`-- collections   <---  Possibly create symlinks for thematic organisation of references (currently unimplemented)
```
The central idea is that each reference has a (meaningfully named) directory below `all` (with `to_read` being the reference's location upon creation). A suggested directory naming scheme is *firstAuthorSurname* + *publicationYear* + *firstTitleKeyWord*, for example we might use *turing1936computable* for A.M. Turing's 1936 paper *"On Computable Numbers, with an Application to the Entscheidungsproblem"*.

## Adding a Reference
```
refadd.py -e -s https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf $REFS/all/to_read/turing1936computable
```
creates the directory `turing1936computable` at location `$REFS/all/to_read/` and populates the newly created directory with the specified PDF file (both HTTP(s) URLs and local paths are supported). In addition, the newly created directory is populated with a minimal `ref.ris` file, for storing bibliographic information (e.g. author, title, publication year) in [RIS](https://en.wikipedia.org/wiki/RIS_(file_format)) format. Thus, our directory tree now looks like this:
```
references/
|-- all
|   `-- to_read
|       `-- turing1936computable
|           |-- Turing_Paper_1936.pdf
|           `-- ref.ris
`-- collections
```
In the previous command, the optional `-e` flag further opens `ref.ris` in $EDITOR, for manual entry of bibliographic information. 

Instead of relying solely on manual RIS data entry, it is alternatively possible to fetch RIS data automatically if we provide a DOI:
```
refadd.py -s https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf -i doi:10.1112/plms/s2-42.1.230 $REFS/all/to_read/turing1936computable
```
If we want to add a reference to the `to_read` directory (while saving a bit of typing), the shell alias `ra` achieves the same effect as follows:
```
ra -s https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf -i doi:10.1112/plms/s2-42.1.230 turing1936computable
```
Side note: We can invoke `refadd.py` (or `ra`) multiple times on the same reference identifier (for example, if we want to edit existing bibliographic information, or include additional files.)

## Navigating and Searching References
Use `refsearch.sh` (aliased as `rs`) to search and naviate based on [fzf](https://github.com/junegunn/fzf). You should see something like this:

TODO Add screenshot

The left-hand pane displays a tree of references. Given a selected reference, the right-hand pane displays:
* **Bibliographic information** ('ref.ris')
* **List of files** (e.g. `.txt` files, PDFs)
* **Notes** (`cat` of `.txt` files)

Incremental search (i.e. by typing) is currently applied to:
* Reference identifiers (and reference paths)
* Contents of `ref.ris` for each reference
* Contents of any `.txt` files (e.g. notes) for each reference

Hitting Enter ↵ opens a shell at the selected directory.

Hitting F1 opens the first PDF (if available), given a selected reference. By contrast, selecting an ancestral directory with multiple references (each with a PDF) causes all such PDFs to be opened simultaneously (useful for reviewing literature).

# Roadmap
* Collections
* Full-text search / keyword extraction
