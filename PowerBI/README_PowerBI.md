# Power BI notes

1. Open Power BI Desktop and choose **Get Data > Text/CSV** for each file under `data/synthetic/`.
2. Use the same model relationships as in the Mermaid ERD from the main README.
3. Recommended visuals:
   - Revenue by country over time (line chart) using `orders`.
   - Category mix by country (stacked column) using `order_items` joined to `products`.
   - Funnel (visit → signup → purchase) using `events`.
   - A/B test lift chart using `marketing_experiments` with separate series for groups A and B.
4. Apply the `model_theme.json` in **View > Themes > Browse for themes** for a dark, high-contrast palette.
