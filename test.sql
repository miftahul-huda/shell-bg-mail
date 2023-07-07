DECLARE v_date_validation DATE;
DECLARE v_data DATE;
SET v_date_validation = '2022-01-01';

SELECT CURRENT_DATETIME('Asia/Jakarta') as START_TIME;

DROP TABLE IF EXISTS cvm-cloud-dwh-prod-4383.prd_temp_tb.mf_11_blacklist;
CREATE TABLE cvm-cloud-dwh-prod-4383.prd_temp_tb.mf_11_blacklist AS
SELECT node,msisdn FROM cvm-cloud-dwh-prod-4383.dev_exc_campaign.cvm_ops_global_exclusion_v3
where REGEXP_CONTAINS(node, 'GCG|Non_EIR|OutsourceNo|Personal VIP|POST|Premium Regular|Premium VIP|Prepaid Premium|Tourist|WLSMS|BOD|XLKita|ENTERPRISE')
;