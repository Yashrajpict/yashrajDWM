# Retail Sales Data Mart, Data Cube and OLAP in Apache Hop

Pipeline file: `retail_sales_datamart_etl_olap.hpl`

This pipeline covers Assignment 2: building a data cube, applying OLAP operations, and creating a sales data mart with an ETL process, using a retail dataset.

Note: the pipeline has not been tested in Apache Hop by its author. If a transform shows an error when opened, note the transform name, error text and Hop version.

## What the pipeline does

| Stage | Transforms | Output |
|-------|-----------|--------|
| Extract | Data Grid (24 retail orders) | Raw sales rows |
| Transform | Calculator, Value Mapper, Select Values, Sort Rows | `sales_amount`, `order_year`, `order_month`, `quarter` |
| Load (data mart, star schema) | Text file output | `dim_product`, `dim_store`, `dim_date`, `dim_customer`, `fact_sales` |
| Data cube | Sort Rows, Group By | `cuboid_base` (category x region x year x quarter) |
| Roll-up | Group By | `rollup_category_year`, `rollup_region` |
| Apex cuboid | Group By | `cuboid_apex` (grand total) |
| Slice | Filter Rows | `slice_west` (region = West) |
| Dice | Filter Rows (two filters) | `dice_electronics_2026` (category = Electronics, year = 2026) |

Drill-down: the base cuboid is the detailed level; the roll-ups show the reverse direction.

## Requirements

- Java 17
- Apache Hop (download from https://hop.apache.org)

## Steps to run

1. **Install and start Hop**
   - Unzip Hop.
   - Run `hop-gui.bat` (Windows) or `./hop-gui.sh` (Linux/Mac).

2. **Create a project**
   - Use the project dropdown at the top left, then **New project**.
   - Name it `retail_datamart` and choose a home folder, for example `C:\hop_projects\retail_datamart`.

3. **Add the pipeline**
   - Unzip the downloaded file to get `retail_sales_datamart_etl_olap.hpl`.
   - Copy it into the project home folder (or its `pipelines` subfolder).
   - In Hop GUI, use File -> Open (or the file explorer on the left) and open the `.hpl` file. The canvas shows about 33 transforms.

4. **Check the output folder**
   - Click an empty spot on the canvas, then Edit -> Pipeline properties -> Parameters.
   - `OUTPUT_DIR` defaults to `${PROJECT_HOME}/output`. Change it if you want the CSV files elsewhere.

5. **Run**
   - Click Run and select the **local** run configuration, then Launch.
   - If none exists: Metadata -> Pipeline Run Configuration -> New, type "Native local".
   - In the Transform metrics panel, every transform should finish with a green tick.

6. **Check the results**
   - Open the `output` folder. It should contain 12 CSV files:
     `dim_product`, `dim_store`, `dim_date`, `dim_customer`, `fact_sales`, `cuboid_base`, `cuboid_apex`, `rollup_category_year`, `rollup_region`, `slice_west`, `dice_electronics_2026`.
   - To preview data without opening files, click a transform and choose Preview (or Data in the metrics panel).

## For the assignment write-up

- **ETL:** describe Extract (Data Grid), Transform (Calculator, Value Mapper, Select Values, Sort Rows) and Load (Text file output).
- **Data mart:** the fact table plus four dimensions form a star schema. The fact table uses natural keys rather than surrogate keys.
- **Cube:** `cuboid_base` is the base cuboid; the roll-ups and apex are higher-level cuboids.
- **OLAP operations and query:** use the roll-up, slice and dice outputs. Add screenshots of the canvas and of each transform preview.

## Troubleshooting

- **Unknown transform or load error:** note the error text and Hop version, and fix or replace that transform.
- **No output files:** check `OUTPUT_DIR` and that the folder is writable.
- **Group By complains about sorting:** make sure the Sort Rows transforms before the Group By transforms are still connected.
- **File will not open in Hop:** make sure the file extension is `.hpl` (not `.hpl.txt`) and that it sits inside the project folder.
