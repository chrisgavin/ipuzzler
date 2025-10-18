import argparse
import json
import pathlib

import ipuzzler.format
import ipuzzler.grid

def parse_arguments():
	parser = argparse.ArgumentParser(
		description="A tool to convert an image of a crossword and list of clues into an ipuz file."
	)
	parser.add_argument(
		"grid",
		help="The path to the image file containing the grid.",
		type=pathlib.Path,
	)
	parser.add_argument(
		"--author",
		help="The author of the crossword.",
		type=str,
	)
	parser.add_argument(
		"--title",
		help="The title of the crossword.",
		type=str,
	)
	parser.add_argument(
		"--dimensions",
		help="The dimensions of the crossword.",
		type=str,
	)
	return parser.parse_args()

def main():
	arguments = parse_arguments()

	puzzle = ipuzzler.format.IPUZCrosswordFile()

	puzzle.author = arguments.author or input("Author: ")
	puzzle.title = arguments.title or input("Title: ")
	dimensions = arguments.dimensions or input("Dimensions: ")
	width, height = dimensions.split("x")
	puzzle.dimensions = ipuzzler.format.Dimensions(int(width), int(height))

	print("Enter clues. Ctrl-D to end:")
	errors = []
	current_direction = puzzle.clues.across
	current_clue = None
	while True:
		try:
			clue = input()
		except EOFError:
			break
		if clue.strip().lower() == "across":
			current_direction = puzzle.clues.across
			continue
		if clue.strip().lower() == "down":
			current_direction = puzzle.clues.down
			continue

		if current_clue is None:
			number = clue.split(" ")[0]
			if not number.isdigit():
				errors += [f"Expected \"{clue}\" to start with a clue number."]
				continue
			current_clue = clue
		else:
			current_clue += " " + clue

		if current_clue.endswith(")"):
			number, text = current_clue.split(" ", 1)
			current_direction.append(ipuzzler.format.Clue(int(number), text))
			current_clue = None

	if errors:
		for error in errors:
			print(f" - {error}")
		raise SystemExit("Errors encountered parsing clues.")

	grid = ipuzzler.grid.parse_grid(arguments.grid, puzzle.dimensions.width, puzzle.dimensions.height)
	puzzle.puzzle = grid

	output = pathlib.Path(f"{puzzle.author} - {puzzle.title}.ipuz")
	with open(output, "w") as output_file:
		json.dump(puzzle, output_file, cls=ipuzzler.format.Encoder, indent="\t")

	print(f"Wrote {output}.")

if __name__ == "__main__":
	main()
