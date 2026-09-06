import test from 'node:test';
import assert from 'node:assert/strict';
import { nextLane, speedAt, flightSpeed, crossesPlayer, intersectsPlayer, calculateScore } from './rules.js';
test('movement clamps at both edges', () => { assert.equal(nextLane(0,-1),0); assert.equal(nextLane(2,1),2); assert.equal(nextLane(1,-1),0); });
test('swept collision catches objects crossing the ship between frames', () => { assert.equal(crossesPlayer(4,7),true); assert.equal(crossesPlayer(6,7),false); assert.equal(crossesPlayer(2,4),false); });
test('adjacent lanes are safe; overlapping hazard hits', () => { assert.equal(intersectsPlayer(0,3.2,'rock'),false); assert.equal(intersectsPlayer(0,.5,'rock'),true); assert.equal(intersectsPlayer(0,0,'energy'),true); });
test('score awards energy and elapsed survival, with capped difficulty', () => { assert.equal(calculateScore(12.6,3),426); assert.equal(speedAt(1000),42); assert.equal(speedAt(0),18); });

test('boost changes actual flight speed, clamps input, and returns to cruise', () => {
  assert.equal(flightSpeed(0, 0), 18);
  assert.equal(flightSpeed(0, 1), 40.5);
  assert.equal(flightSpeed(0, 2), 40.5);
  assert.equal(flightSpeed(0, -1), 18);
});
