"""
BigQuery Query for Get Data from Gdeltv2 table
SELECT 
  DISTINCT(SQLDATE), 
  SOURCEURL as url, 
  ActionGeo_CountryCode as country 
FROM 
  `gdelt-bq.full.events` 
WHERE 
  (
    LOWER(Actor1Name) LIKE '%mpox%' 
    OR LOWER(Actor1Name) LIKE '%monkeypox%' 
    OR LOWER(Actor1Name) LIKE '%viruela del mono%' 
    OR LOWER(Actor2Name) LIKE '%mpox%' 
    OR LOWER(Actor2Name) LIKE '%monkeypox%' 
    OR LOWER(Actor2Name) LIKE '%viruela del mono%' 
    OR LOWER(SOURCEURL) LIKE '%mpox%' 
    OR LOWER(SOURCEURL) LIKE '%monkeypox%' 
    OR LOWER(SOURCEURL) LIKE '%viruela%'
  )
  AND (
    LOWER(ActionGeo_FullName) LIKE '%latin america%' 
    OR ActionGeo_CountryCode IN ('MEX', 'ARG', 'BRA', 'COL', 'CHL', 'PER',"PAR","URU","BOL") 
    OR LOWER(ActionGeo_FullName) LIKE '%mexico%' 
    OR LOWER(ActionGeo_FullName) LIKE '%argentina%' 
    OR LOWER(ActionGeo_FullName) LIKE '%brasil%' 
    OR LOWER(ActionGeo_FullName) LIKE '%colombia%'
  ) 
  AND SQLDATE BETWEEN 20190101 AND 20240901
ORDER BY 
  SQLDATE DESC 

  
"""