# Copyright (C) 2020-2025 Luceda Photonics
# This version of Luceda Academy and related packages
# (hereafter referred to as Luceda Academy) is distributed under a proprietary License by Luceda
# It does allow you to develop and distribute add-ons or plug-ins, but does
# not allow redistribution of Luceda Academy  itself (in original or modified form).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# For the details of the licensing contract and the conditions under which
# you may use this software, we refer to the
# EULA which was distributed along with this program.
# It is located in the root of the distribution folder.


def _list_duplicates(seq):
    """Finds duplicates in a list"""
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)


def all_designs_have_unique_prefix(designs):
    """Checks for the uniqueness of the prefix
    :param designs: list of designs
    :return: True
    """
    prefixes = [d["prefix"] for d in designs]
    duplicates = _list_duplicates(prefixes)
    if len(duplicates) > 0:
        warning = f"""
The following prefixes occur twice - this is not allowed as it might lead to colliding GDSIInames
{duplicates}
        """  # fmt: skip
        raise Exception(warning)
    return True


checks = [all_designs_have_unique_prefix]
