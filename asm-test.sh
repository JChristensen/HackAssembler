#!/bin/bash
# Test Hack assembler.
# Files named *1.hack are output from the supplied assembler.
# Files named *.hack are output from my assembler.

rm -f add/Add.hack max/Max.hack max/MaxL.hack rect/Rect.hack rect/RectL.hack pong/Pong.hack pong/PongL.hack

hackasm add/Add.asm >/dev/null
git diff --no-index add/Add1.hack add/Add.hack

hackasm max/Max.asm >/dev/null
hackasm max/MaxL.asm >/dev/null
git diff --no-index max/Max1.hack max/Max.hack
git diff --no-index max/MaxL1.hack max/MaxL.hack

hackasm rect/Rect.asm >/dev/null
hackasm rect/RectL.asm >/dev/null
git diff --no-index rect/Rect1.hack rect/Rect.hack
git diff --no-index rect/RectL1.hack rect/RectL.hack

hackasm pong/Pong.asm >/dev/null
hackasm pong/PongL.asm >/dev/null
git diff --no-index pong/Pong1.hack pong/Pong.hack
git diff --no-index pong/PongL1.hack pong/PongL.hack
