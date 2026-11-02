# Data model and transformations

## Source grains
| File | Grain | Key |
|---|---|---|
| olist_orders_dataset.csv | Order | order_id |
| olist_order_items_dataset.csv | Item line | order_id + order_item_id |
| olist_order_payments_dataset.csv | Payment event | order_id, repeated |
| olist_order_reviews_dataset.csv | Review event | order_id, repeated |
| olist_customers_dataset.csv | Customer lookup | customer_id |
| olist_sellers_dataset.csv | Marketplace seller | seller_id |
| olist_products_dataset.csv | Product | product_id |
| product_category_name_translation.csv | Category mapping | product_category_name |

## Join design
- ORDERS one-to-many ORDER_ITEMS, PAYMENTS and REVIEWS.
- ORDER_ITEMS many-to-one PRODUCTS and SELLERS.
- ORDERS many-to-one CUSTOMERS.
- PRODUCTS many-to-one CATEGORY_TRANSLATION.

Never directly join raw item and payment rows and then sum amounts: an order with two item lines and two payments would be multiplied into four rows.

## Transformation
1. Validate required headers and unique primary keys.
2. Read original Olist records without making up missing dates, prices or quantities.
3. Aggregate item price and freight to order_id, and independently to seller and category.
4. Aggregate payments to order_id and review scores to one order-level average.
5. Join derived values to unique orders and compute eligibility, delivery delay and purchase-month cohort.
6. Produce order-level, monthly, seller and category CSVs plus a QA JSON summary.
7. Build Excel reporting from the produced tables.

## Data boundaries
Seller-attributed order counts can overlap across sellers and cannot be summed into platform unique orders. Customer payments do not represent procurement spend. The source contains no upstream purchase orders or goods receipt events. Avoid combining synthetic NZ Purchasing data and real Olist rows as if one company generated them.
