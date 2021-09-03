# import argparse

# def argument_parser():
#     parser = argparse.ArgumentParser(description='Dataset uploader for IoT.own')
#     parser.add_argument("-l", "--list", help="get list of dataset in IoT.own",action="store_true")
#     parser.add_argument("-d", "--dataset", help="dataset names ex) coco2017, voc2012, voc2007")
#     parser.add_argument("-t", "--token", help="you must input api token for using IoT.own API")
#     parser.add_argument("-u", "--url", help="IoT.own Server URL ex) http://192.168.0.224")
#     return parser.parse_args()

# if __name__ == "__main__":
#     args = argument_parser()
#     if args.dataset == "":
#         cocodataset()
#     elif args.dataset == "":   
#         vocdataset()
#     elif args.dataset == "":