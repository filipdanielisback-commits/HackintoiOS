# Display drivers

This directory is reserved for display-controller, panel, and framebuffer handoff support.

Current status: not implemented. The exact XT2135-2 panel/module variant, display controller path, timing, reset sequence, and firmware handoff are not yet verified.

The first safe milestone is a documented display-resource contract. Do not write panel registers or claim GPU/display acceleration from the Adreno research alone.
