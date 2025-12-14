import pathlib
import typing

import numpy
import PIL.Image

def parse_grid(image_path: pathlib.Path, width:int, height:int) -> typing.List[typing.List[typing.Union[int, str]]]:
	grid = image_to_grid(image_path, width, height)
	return annotate_grid(grid)

def annotate_grid(grid: typing.List[typing.List[bool]]) -> typing.List[typing.List[typing.Union[int, str]]]:
	annotated_grid: typing.List[typing.List[typing.Union[int, str]]] = []
	clue_number = 1
	for y in range(len(grid)):
		row: typing.List[typing.Union[int, str]] = []
		for x in range(len(grid[0])):
			if not grid[y][x]:
				row.append("#")
				continue

			is_start_of_across = (
				(x == 0 or not grid[y][x - 1])
				and (x + 1 < len(grid[0]) and grid[y][x + 1])
			)
			is_start_of_down = (
				(y == 0 or not grid[y - 1][x])
				and (y + 1 < len(grid) and grid[y + 1][x])
			)

			if is_start_of_across or is_start_of_down:
				row.append(clue_number)
				clue_number += 1
			else:
				row.append(0)
		annotated_grid.append(row)
	return annotated_grid

def image_to_grid(image_path: pathlib.Path, width:int, height:int) -> typing.List[typing.List[bool]]:
	image = PIL.Image.open(image_path).convert("L")
	lookup_table = [0 if i <= 64 else 255 for i in range(256)]
	image = image.point(lookup_table)
	image_data = numpy.array(image)

	cell_width = image_data.shape[1] // width
	cell_height = image_data.shape[0] // height
	cells = []
	for y in range(height):
		row = []
		for x in range(width):
			cell_data = image_data[
				y * cell_height : (y + 1) * cell_height,
				x * cell_width : (x + 1) * cell_width,
			]
			black_pixel_count = numpy.sum(cell_data == 0)
			total_pixel_count = cell_data.size
			row.append(black_pixel_count / total_pixel_count < 0.5)
		cells.append(row)

	return cells
