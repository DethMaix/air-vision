export const getRagiusFromZoom = (zoom: number): number => {
  const MIN_RADIUS = 20;
  const MAX_RADIUS = 2000;

  const baseRadius = 500;
  const baseZoom = 5;

  const radius = baseRadius / 2 ** (zoom - baseZoom);

  return Math.min(MAX_RADIUS, Math.max(radius, MIN_RADIUS));
};
