# License Options

Packaging OS contains both workflow/code-like materials and design-process writing, so the license choice should be deliberate.

## Recommended Simple Option

Use `MIT License` for the whole repository if the goal is broad adoption and low friction.

Good for:

- Claude Skills
- scripts
- templates
- workflow docs
- forks and adaptations

Tradeoff:

- Others can reuse the system commercially with attribution and without sharing improvements back.

## More Protective Documentation Option

Use a dual license:

- `MIT License` for scripts and Claude Skills
- `Creative Commons Attribution 4.0 International` for docs, templates, and methodology writing

Good for:

- clearer attribution around the written framework
- still allowing broad reuse

Tradeoff:

- slightly more explanation in the README
- more maintenance overhead when contributors add new files

## Copyleft Option

Use `GPL-3.0` or `AGPL-3.0` only if you want derivatives to share source under the same license.

Good for:

- forcing open derivatives

Tradeoff:

- many teams avoid GPL/AGPL content in commercial workflows
- less friendly for a design-studio operating system intended to spread

## Current Decision

The first public release uses MIT unless this file is revised before publication.

The root `LICENSE` file uses `Packaging OS contributors` as the copyright holder.
