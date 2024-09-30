from pathlib import Path

import rapidfuzz


class Lookup:
    # TODO this is the naive implementation, as a proof of concept, of course we can make it faster later

    def __init__(self, entries_list: list[dict[str, str]]):
        self._entries_list = entries_list

    @property
    def entries_list(self) -> list[dict[str, str]]:
        return self._entries_list

    def exists(self, entry: dict[str, str]) -> bool:
        for entry_ in self._entries_list:
            if entry["dir"] == entry_["dir"] and entry["name"] == entry_["name"]:
                return True
        return False

    def fuzzy_match(
        self, entry: dict[str, str], n_max: int
    ) -> list[tuple[str, float, int]]:
        # prepare the inputs
        entry_path = str(Path(entry["dir"]) / entry["name"])
        entries_list_paths = [
            str(Path(entry_["dir"]) / entry_["name"]) for entry_ in self._entries_list
        ]

        # find the best matches
        return rapidfuzz.process.extract(
            entry_path, entries_list_paths, scorer=rapidfuzz.fuzz.WRatio, limit=n_max
        )

    def print_fuzzy_matches(
        self,
        entry: dict[str, str],
        template: str,
        threshold: float = 90,
        n_max: int = 5,
    ):
        for file, score, index in self.fuzzy_match(entry=entry, n_max=n_max):
            if score >= threshold:
                entry = self._entries_list[index]
                print(template.format(**entry, score=score))

    def __iter__(self):
        return iter(self._entries_list)

    def __len__(self):
        return len(self._entries_list)
