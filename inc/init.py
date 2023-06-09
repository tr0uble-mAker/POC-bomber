from inc import common, config, output
import platform, queue

def init_all():
    output.logo()
    args = common.get_parser()
    common._init()
    poc_path, poc_list = common.do_path(args.poc)
    common.set_value("tr0uble_mAker", True)
    common.set_value("os", "windows" if "Windows" in platform.system() else "linux")
    common.set_value("show_progress", True if config.show_progress else False)
    common.set_value("show", True if args.show else False)                                          # --show
    common.set_value("output_path", args.output if args.output else config.output_path)             # --output
    common.set_value("max_threads", args.threads if args.threads else config.max_threads)           # --threads
    common.set_value("timeout", args.timeout if args.timeout else config.timeout)                   # --timeout
    common.set_value("delay", args.delay if args.delay else config.delay)                           # --delay
    common.set_value('dnslog_flag', True if args.dnslog else False)                                 # --dnslog
    common.set_value('attack', True if args.attack else False)                                      # --attack
    common.set_value("target_list", [args.url] if args.url else common.get_target_list(args.file))  # --url,--file
    common.set_value("pocinfo_dict", common.get_pocinfo_dict())
    common.set_value("script_list", common.get_poc_scriptname_list_by_search(poc_path, poc_list))
    common.set_value("total_times", len(common.get_value("target_list"))*len(common.get_value("script_list")))
    common.set_value("current_times", 0)
    common.set_value("success_times", 0)
    common.set_value("output_queue", queue.Queue())
    common.set_value("exit_queue", queue.Queue())
    common.set_value("success_list", [])
    '''dnslog参数'''
    common.set_value("dnslog_base_domain", config.dnslog_base_domain)
    common.set_value("dnslog_is_auth", config.dnslog_is_auth)
    common.set_value("dnslog_auth_token", config.dnslog_auth_token)
    common.set_value("dnslog_web_port", config.dnslog_web_port)
    common.set_value("dnslog_server_ip", config.dnslog_server_ip)
    common.set_value("dnslog_scan_dict", {})

if not common.get_value("tr0uble_mAker"):
    init_all()