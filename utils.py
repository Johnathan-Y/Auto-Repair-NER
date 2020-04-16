import logging, sys, argparse


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    PER = get_PER_entity(tag_seq, char_seq)
    LOC = get_LOC_entity(tag_seq, char_seq)
    ORG = get_ORG_entity(tag_seq, char_seq)
    return PER, LOC, ORG


def get_PER_entity(tag_seq, char_seq):
    length = len(char_seq)
    PER = []
    print('字符序列',char_seq)
    print('标签序列',tag_seq)

    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        print('i，locals().keys()', i,locals().keys())
        if tag == 'B-CAR':
            if 'per' in locals().keys():
                PER.append(per)
                del per
            per = char
            if i+1 == length:
                PER.append(per)
        if tag == 'I-CAR':
            per += char
            if i+1 == length:
                PER.append(per)
        if tag not in ['I-CAR', 'B-CAR']:
            if 'per' in locals().keys():
                PER.append(per)
                del per
            continue
    return PER


def get_LOC_entity(tag_seq, char_seq):
    length = len(char_seq)
    LOC = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-CPT':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)
        if tag == 'I-CPT':
            loc += char
            if i+1 == length:
                LOC.append(loc)
        if tag not in ['I-CPT', 'B-CPT']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC


def get_ORG_entity(tag_seq, char_seq):
    length = len(char_seq)
    ORG = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-BRD':
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            org = char
            if i+1 == length:
                ORG.append(org)
        if tag == 'I-BRD':
            org += char
            if i+1 == length:
                ORG.append(org)
        if tag not in ['I-BRD', 'B-BRD']:
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            continue
    return ORG


def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
