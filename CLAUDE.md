# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Steam Bundle Generator - a tool that generates Steam store bundle images from two game URLs.

## Program Flow

1. Accept two Steam store page URLs as input
2. Scrape game names from both pages
3. Create output folder named `{game1}_x_{game2}`
4. Scrape "Main Capsule" store images for both games, save as `game1.png` and `game2.png`
5. Concatenate images with `cross.png` in between (image1 × image2 layout) and scale to generate four required bundle image sizes

## Image Concatenation

Uses Pillow to combine images horizontally: `[game1] [cross.png] [game2]`

The `cross.png` asset is placed between the two game capsule images to create the bundle visual.

## Required Output Images

| Image Type | Dimensions |
|------------|------------|
| Package Header | 1414×464 px |
| Header Capsule | 920×430 px |
| Small Capsule | 462×174 px |
| Main Capsule | 1232×706 px |

## Running

```bash
python gen.py
```

## Dependencies

Likely needs: `requests`, `beautifulsoup4`, `Pillow` (PIL) for web scraping and image manipulation.
