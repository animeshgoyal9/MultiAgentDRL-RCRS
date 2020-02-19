#!/usr/bin/env python3

import subprocess, sys, argparse, socket


def run(algorithm):
	print(algorithm)
	# columns = ['Mean Rewards', 'Standard deviation'] 
	# df = pd.DataFrame(columns=columns)
	# df.to_csv("{}_{}_{}".format(algorithm, hostname, "MeanAndStdReward.csv", sep=',',index=True))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("algorithm", help = 'Which algorithm are you using', type= str)
	args = parser.parse_args()
	run(args.algorithm)

if __name__ == '__main__':
	main()