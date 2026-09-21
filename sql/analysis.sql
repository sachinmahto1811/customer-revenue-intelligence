-- Net revenue and return rate
SELECT
  SUM(net_revenue) AS net_revenue,
  AVG(CASE WHEN return_amount > 0 THEN 1.0 ELSE 0 END) AS return_rate
FROM orders;

-- Repeat customer behavior
SELECT
  customer_id,
  COUNT(*) AS order_count,
  SUM(net_revenue) AS lifetime_net_revenue
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY lifetime_net_revenue DESC;

-- Acquisition channel value
SELECT
  c.acquisition_channel,
  COUNT(DISTINCT o.customer_id) AS customers,
  SUM(o.net_revenue) AS net_revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.acquisition_channel
ORDER BY net_revenue DESC;
