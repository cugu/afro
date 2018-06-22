import csv
import collections
import sys
import os
import logging

from afro import log


LOGGER = logging.getLogger(__name__)


class Matchor:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def matches(self, key):
        return self.a[key] == self.b[key]


def format_row(prefix, item, suffix=""):
    return "%s %10s %3s %8s %-10s %-10s %10s %4s %s %s %s" % (
        prefix,
        item['volume'],
        item['id'],
        item['type'],
        "…" + item['mtime'][6:15] + "…",
        "…" + item['crtime'][6:15] + "…",
        item['size'],
        item['md5'][:4],
        item['path'].replace('/root/', ''),
        item['name'],
        suffix
    )

def compare(arg):

    gtffile = os.path.abspath(arg)

    for ending in [
            'dmg.parse.gtf',
            'dmg.carve_nxsb.gtf',
            'dmg.carve_apsb.gtf',
            'dmg.carve_nodes.gtf'
    ]:

        extrfile = arg.replace('generation.gtf', ending)
        if not os.path.exists(extrfile):
            LOGGER.error("%s not found.", extrfile)
            continue

        full_matches = collections.Counter()
        filename_matches = collections.Counter()
        content_matches = collections.Counter()
        metadata_matches = collections.Counter()
        total = collections.Counter()
        categories = set()

        with open(gtffile) as gtf_io:
            gtf_reader = csv.DictReader(gtf_io)
            for gtf_row in gtf_reader:

                category = "%s:%s" % (gtf_row['type'], gtf_row['status'])
                categories.add(category)
                total[category] += 1
                matched = False

                possible_matches = list()

                filename_matched = False
                content_matched = False
                metadata_matched = False

                with open(extrfile) as extr_io:
                    extr_reader = csv.DictReader(extr_io)
                    for extr_row in extr_reader:

                        m = Matchor(gtf_row, extr_row)

                        volume_unknown = extr_row['volume'] == 'unknown'
                        if m.matches('id') and (m.matches('volume') or volume_unknown):

                            filename_matched_row = False
                            content_matched_row = False
                            metadata_matched_row = False

                            # filename matches?
                            path_matches = gtf_row['path'] == extr_row['path'].replace('/root', '')[1:]
                            root_name_matches = gtf_row['name'] == '' and extr_row['name'] == 'root'
                            if m.matches('name') or root_name_matches: # and path_matches: TODO
                                filename_matched = True
                                filename_matched_row = True

                            # timestamps match?
                            if m.matches('mtime') and m.matches('crtime'):
                                metadata_matched = True
                                metadata_matched_row = True

                            # content matches?
                            if gtf_row['type'] == 'file' and m.matches('size') and m.matches('md5'):
                                content_matched = True
                                content_matched_row = True

                            if filename_matched_row and metadata_matched_row and (content_matched_row or gtf_row['type'] == 'folder'):
                                matched = True
                                break
                            else:
                                possible_matches.append(extr_row)

                    if matched:
                        full_matches[category] += 1
                        filename_matches[category] += 1
                        if gtf_row['type'] == 'file':
                            content_matches[category] += 1
                        metadata_matches[category] += 1
                    else:
                        if filename_matched:
                            filename_matches[category] += 1
                        if content_matched:
                            content_matches[category] += 1
                        if metadata_matched:
                            metadata_matches[category] += 1

                        if gtf_row['status'] == 'active':
                            msg = list()
                            if not filename_matched:
                                msg.append("filename mismatch")
                            if gtf_row['type'] == 'file' and not content_matched:
                                msg.append("content mismatch")
                            if not metadata_matched:
                                msg.append("metadata mismatch")

                            LOGGER.warning(format_row("   ", gtf_row, ", ".join(msg)))
                            for possible_match in possible_matches:
                                LOGGER.warning(format_row("-> ", possible_match))


        msg = "Found items in %s:\n" % (extrfile)
        for category in sorted(categories):
            msg += '%24s: %4d (name: %4d, metadata: %4d, content: %4d) of %4d (%5.1f%%)\n' % (
                category,
                full_matches[category],
                filename_matches[category],
                metadata_matches[category],
                content_matches[category],
                total[category],
                (full_matches[category] / total[category]) * 100
            )

        msg += '%24s: %4d (name: %4d, metadata: %4d, content: %4d) of %4d (%5.1f%%)\n' % (
            'all categories',
            sum(full_matches.values()),
            sum(filename_matches.values()),
            sum(metadata_matches.values()),
            sum(content_matches.values()),
            sum(total.values()),
            (sum(full_matches.values()) / sum(total.values())) * 100
        )

        print(msg)

def main():
    # setup logging
    log.set_logging(sys.argv[1])
    for arg in sys.argv[2:]:
        compare(arg)

if __name__ == '__main__':
    main()

