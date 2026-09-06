export const LANES = [-3.2, 0, 3.2];
export const SHIP_Z = 5;
export function nextLane(lane, direction) { return Math.max(0, Math.min(2, lane + direction)); }
export function speedAt(seconds) { return Math.min(42, 18 + seconds * 0.22); }
export function flightSpeed(seconds, boost) { return speedAt(seconds) * (1 + Math.max(0, Math.min(1, boost)) * 1.25); }
export function crossesPlayer(previousZ, z) { return previousZ < SHIP_Z && z >= SHIP_Z; }
export function intersectsPlayer(playerX, objectX, kind) { return Math.abs(playerX - objectX) < (kind === 'energy' ? 1.15 : 1.3); }
export function calculateScore(seconds, energy) { return Math.floor(seconds * 10) + energy * 100; }
