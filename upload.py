import argparse
import lib.vocdataset as vocdataset
import lib.cocodataset as cocodataset
import lib.customdataset as customdataset
support = [ "coco2017" , "voc2012", "voc2007", "custom"]
def argument_parser():
    parser = argparse.ArgumentParser(description='Dataset uploader for IoT.own')
    parser.add_argument("-d", "--dataset", help="dataset names ex) coco2017, voc2012, voc2007", required=True)
    parser.add_argument("-t", "--token", help="you must input api token for using IoT.own API", required=True) 
    parser.add_argument("-u", "--url", help="IoT.own Server URL ex) http://192.168.0.224", required=True)
    parser.add_argument("-l", "--label", help="Dataset Class ex) person, car, airplane", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    print("#############################")
    print("# Upload Dataset To IoT.own #")
    print("#############################")
    print("currently support --------------")
    print(support)
    args = argument_parser()
    if args.dataset == "coco2017":
        cocodataset.upload_dataset(args.url, args.token, args.label)
    elif args.dataset == "voc2007":   
        vocdataset.upload_dataset(args.url, args.token, args.label,"voc2007")
    elif args.dataset == "voc2012":
        vocdataset.upload_dataset(args.url, args.token, args.label,"voc2012")
    elif args.dataset == "custom":
        customdataset.upload_dataset(args.url, args.token, args.label)
    else:
        print(args.dataset,"is Currently Not Support")