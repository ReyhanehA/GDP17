from dogshell.common import report_errors, report_warnings, CommandLineClient, find_localhost
from dogapi.constants import MetricType

class MetricClient(CommandLineClient):

    def setup_parser(self, subparsers):
        parser = subparsers.add_parser('metric', help='Post metrics.')
        verb_parsers = parser.add_subparsers(title='Verbs')

        post_parser = verb_parsers.add_parser('post', help='Post metrics')
        post_parser.add_argument('name', help='metric name')
        post_parser.add_argument('value', help='metric value (integer or decimal value)', type=float)
        post_parser.add_argument('--host', help='scopes your metric to a specific host', default=None)
        post_parser.add_argument('--device', help='scopes your metric to a specific device', default=None)
        post_parser.add_argument('--tags', help='comma-separated list of tags', default=None)
        post_parser.add_argument('--localhostname', help='same as --host=`hostname` (overrides --host)', action='store_true')
        post_parser.add_argument('--counter', help='submit value as a uint64 counter instead of gauge', action='store_false')
        parser.set_defaults(func=self._post)


    def _post(self, args):
        self.dog.timeout = args.timeout
        if args.localhostname:
            host = find_localhost()
        else:
            host = args.host
        if args.tags:
            tags = sorted(set([t.strip() for t in
                               args.tags.split(',') if t]))
        else:
            tags = None

        # are we sending a counter?
        if args.counter:
            metric_type = MetricType.Counter
        else:
            metric_type = MetricType.Gauge
        res = self.dog.metric(args.name, args.value, host=host,
            device=args.device, tags=tags, metric_type=metric_type)
        report_warnings(res)
        report_errors(res)
