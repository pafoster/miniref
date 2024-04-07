# What is miniref?
miniref is an recreational experiment at creating an **academic reference manager** (in the sense of [Zotero](https://www.zotero.org)), but for the **command line** and with a **minimalist flavour**. It is strongly inspired by projects like [Cobib](https://mrossinek.gitlab.io/programming/introducing-cobib/) and [fast-p](https://github.com/bellecp/fast-p). 

## Tutorial
We will use the following bare directory structure for storing our references:
```
references/
|-- all
|   `-- to_read
`-- collections
```
The central idea is that each reference has a (meaningfully named) directory below `all` (with `to_read` being the initial location of the reference upon creation). A suggested directory naming scheme is *firstAuthorSurname* + *publicationYear* + *firstTitleKeyWord*, for example we might use *turing1936computable* for A.M. Turing's 1936 paper *"On Computable Numbers, with an Application to the Entscheidungsproblem"*.

### Adding a Reference
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
### Searching and Navigating References
