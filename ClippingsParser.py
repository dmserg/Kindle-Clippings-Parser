import sys


def mapper(mr, record):
    if record['type'] == 'Highlight':
        mr.emit_intermediate(record['title'], record['body'])


def reducer(mr, key, records):
    record = dict()
    record['Quotes'] = records
    record['Title'] = key
    mr.emit(record)


class ClippingsParser:
    def __init__(self):
        self.EOR = u"=========="

    def clippingRecords(self, file_path):
        import re
        import codecs
        clip_file = codecs.open(file_path)
        clip_file.seek(3)  # skip magic cookie

        record = list()
        for line in clip_file:
            line = line.decode('utf-8')
            if line.strip() == self.EOR:
                assert record[2] == '', u"Non-blank line expected separating the header from the body of the clipping:{0:s}" \
                    .format(record[2])
                clip = dict()
                match = re.match(r'(.*?)\(([^(]*)\)$', record[0])
                if match:
                    clip['title'], clip['attribution'] = match.groups()
                    clip['attribution'] = clip['attribution'].split(') (')
                else:
                    # pattern isn't matched
                    clip['title'] = record[0]
                    clip['attribution'] = ''

                try:
                    match = re.match(r'- (.+) Loc. ([^|]+)\| Added on (\w+), (\w+ \d+, \d+), (\d+:\d+ \w\w)',
                                     record[1])

                    clip['type'], clip['location'], clip['dow'], clip['date'], clip['time'] = match.groups()

                    clip['body'] = "\n".join(record[3:])

                    # a little tidying
                    clip['title'] = clip['title'].strip()
                    clip['location'] = clip['location'].strip()
                    # yield and reset for next record
                    yield clip
                    record = list()
                except:
                    print("Unexpected error:", sys.exc_info()[0])
            else:
                record.append(line.strip())

        clip_file.close()

    def parseClippings(self, fileName):
        from MapReduce import MapReduce
        mr = MapReduce()
        mr.execute(self.clippingRecords(fileName), mapper, reducer)
        return mr.result
