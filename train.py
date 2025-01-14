# -*- coding: utf-8 -*-#

import os, json, random, re
import numpy as np
import torch
from models.module import ModelManager
from utils.loader import DatasetManager
from utils.process import Processor
from utils.config import *
from priority import priority

if __name__ == "__main__":
    print(args)
    # Save training and model parameters.
    if not os.path.exists(args.save_dir):
        os.system("mkdir -p " + args.save_dir)

    log_path = os.path.join(args.save_dir, "param.json")
    with open(log_path, "w", encoding="utf8") as fw:
        fw.write(json.dumps(args.__dict__, indent=True))

    # Fix the random seed of package random.
    random.seed(args.random_state)
    np.random.seed(args.random_state)

    # Fix the random seed of Pytorch when using GPU.
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.random_state)
        torch.cuda.manual_seed(args.random_state)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    # Fix the random seed of Pytorch when using CPU.
    torch.manual_seed(args.random_state)
    torch.random.manual_seed(args.random_state)

    # Instantiate a dataset object.
    dataset = DatasetManager(args)
    dataset.quick_build()

    # Instantiate a network model object.
    model = ModelManager(
        args, len(dataset.word_alphabet),
        len(dataset.slot_alphabet),
        len(dataset.intent_alphabet),
        args.save_dir
    )

    # To train and evaluate the models.
    process = Processor(dataset, model, args)
    best_epoch = process.train()
    result = Processor.validate(
        os.path.join(args.save_dir, "model/model.pkl"),
        dataset,
        args.batch_size, len(dataset.intent_alphabet), args=args)
    priority()
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    with open(os.path.join(args.log_dir, args.log_name), 'w') as fw:
        fw.write(str(best_epoch) + ',' + str(result))
    print(args.save_dir)
    getinput='y'
    while (getinput!='n'):
        q=input("Enter the query: ")
        qry=re.findall(r"[A-Za-z]+|\S", q)
        f = open(os.path.join(args.data_dir, "userinput.txt"), "w")
        for word in qry:
            f.write(word+' O\n')
        f.close()

        getinput=input("choice: ")

    # inputdataset = DatasetManager()
    # inputdataset.quick_build()
    process.predict(model, dataset, 'userinput', args.batch_size, args)