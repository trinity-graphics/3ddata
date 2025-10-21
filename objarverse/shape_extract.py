import os
import sys

import multiprocessing
import subprocess
import argparse

from functools import partial
from tqdm import tqdm

# module-level blender executable used by the picklable worker
BLENDER_EXEC = None


def _worker_task(task):
	"""Picklable worker wrapper for Pool.imap_unordered.

	`task` is a (src, dst, meta, file_ext) tuple. Uses module-level BLENDER_EXEC.
	"""
	src, dst, meta, file_ext = task
	return _call_blender_worker(BLENDER_EXEC, src, dst, meta, file_ext)

# Path to the worker script that Blender will run in background for each file.
WORKER_SCRIPT = os.path.join(os.path.dirname(__file__), 'shape_extract_worker.py')


def _call_blender_worker(blender_exec, src, dst, meta_path, file_ext):
	cmd = [blender_exec, '--background', '--python', WORKER_SCRIPT, '--', src, dst, meta_path, file_ext]
	try:
		proc = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out = proc.stdout.decode(errors='ignore') if proc.stdout is not None else ''
		return proc.returncode, out
	except FileNotFoundError:
		return 127, f'Blender executable not found: {blender_exec}'


def process_all(input_dir, output_dir, file_ext, blender_exec='blender', jobs=None):
	input_dir = os.path.abspath(input_dir)
	output_dir = os.path.abspath(output_dir)
	os.makedirs(output_dir, exist_ok=True)
	metadata_dir = os.path.join(output_dir, 'metadata')
	os.makedirs(metadata_dir, exist_ok=True)

	raw_files = []
	for root, _, files in os.walk(input_dir):
		for f in files:
			if f.lower().endswith(file_ext):
				raw_files.append(os.path.join(root, f))

	if not raw_files:
		print(f'No {file_ext} files found in {input_dir}')
		return

	jobs = jobs or max(1, round((multiprocessing.cpu_count() - 1) * 0.8))
	print(f'Found {len(raw_files)} {file_ext} files. Running up to {jobs} parallel Blender jobs.')

	# Prepare tasks preserving relative paths
	tasks = []
	for src in raw_files:
		dst = os.path.join(output_dir, os.path.basename(src).replace(file_ext, 'obj'))
		if os.path.exists(dst):
			continue
		dst_dir = os.path.dirname(dst)
		os.makedirs(dst_dir, exist_ok=True)

		meta_dst = os.path.join(metadata_dir, os.path.basename(src).replace(file_ext, 'json'))
		tasks.append((src, dst, meta_dst, file_ext))
	
	if len(tasks) == 0:
		print('All processed files has been existed')
		exit(0)

	# Run Blender jobs in parallel; each task spawns a Blender process
	# set module-level blender exec for worker pickling
	global BLENDER_EXEC
	BLENDER_EXEC = blender_exec

	with multiprocessing.Pool(processes=min(jobs, len(tasks))) as pool:
		results = []
		it = pool.imap_unordered(_worker_task, tasks)
		for r in tqdm(it, total=len(tasks)):
			results.append(r)

	# Report results
	failed = [(tasks[i][0], r) for i, r in enumerate(results) if r[0] != 0]
	if failed:
		print(f"{len(failed)} files failed to process:")
		for src, (code, out) in failed:
			print(f'- {src} (exit {code}) (out: {out})')
	else:
		print('All files processed successfully.')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_dir", required=True, help="input_dir")
	parser.add_argument("--output_dir", required=True, help="output_dir")
	parser.add_argument("--blender_exec", default='blender', help="blender execution")
	parser.add_argument("--jobs", default=4, type=int, help="# Jobs")
	parser.add_argument("--file_ext", required=True, help="file_ext")
	
	args = parser.parse_args()
	process_all(args.input_dir, args.output_dir, args.file_ext, args.blender_exec, args.jobs)