-- 3. Old school band
-- This script lists all Glam rock bands ranked by longevity
SELECT band_name, (2022 - formed) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
