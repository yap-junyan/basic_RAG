from langchain_core.document_loaders import BaseLoader
from langchain_community.document_loaders import Docx2txtLoader
from pathlib import Path
from typing import Union
import logging

logger = logging.getLogger(__file__)


class DocxDirectoryLoader(BaseLoader):
    """Load a directory with `docx` files using `docx2txt` and chunks at character level."""

    def __init__(
        self,
        path: Union[str, Path],
        glob: str = "**/[!.]*.docx",
        silent_errors: bool = False,
        load_hidden: bool = False,
        recursive: bool = False,
    ):
        self.path = path
        self.glob = glob
        self.load_hidden = load_hidden
        self.recursive = recursive
        self.silent_errors = silent_errors

    @staticmethod
    def _is_visible(path: Path) -> bool:
        return not any(part.startswith(".") for part in path.parts)

    def load(self) -> str:
        """Load the docx files in the directory and return the concatenated text."""
        p = Path(self.path)
        docs = []
        items = p.rglob(self.glob) if self.recursive else p.glob(self.glob)
        for i in items:
            if i.is_file():
                if self._is_visible(i.relative_to(p)) or self.load_hidden:
                    try:
                        loader = Docx2txtLoader(str(i))
                        sub_docs = loader.load()
                        for doc in sub_docs:
                            doc.metadata["source"] = str(i)
                        docs.extend(sub_docs)
                    except Exception as e:
                        if self.silent_errors:
                            logger.warning(e)
                        else:
                            raise e
        return docs
