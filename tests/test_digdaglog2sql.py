from digdaglog2sql.extractor import extract_sql
from digdaglog2sql.td_op import extract_td_sql


def test_extract_sql():
    log = """2022-04-30 07:00:04.079 +0000 [INFO] (0184@[1:tbl1:76144781:411862721]+create_database) io.digdag.core.agent.OperatorManager: td_ddl>: 
2022-04-30 07:00:04.153 +0000 [INFO] (0184@[1:tbl1:76144781:411862721]+create_database) io.digdag.standards.operator.td.TdDdlOperatorFactory$TdDdlOperator: Creating TD database tbl1

2022-04-30 07:04:38.245 +0000 [INFO] (0351@[1:tbl1:76144781:411862721]+rename) io.digdag.core.agent.OperatorManager: td_ddl>: 
2022-04-30 07:04:38.582 +0000 [INFO] (0351@[1:tbl1:76144781:411862721]+rename) io.digdag.standards.operator.td.TdDdlOperatorFactory$TdDdlOperator: Renaming TD table tbl1.cdp_tmp_behavior_behavior_1 -> behavior_behavior_1

2022-04-30 07:00:05.910 +0000 [INFO] (0222@[1:tbl1:76144781:411862721]+create_table_customers) io.digdag.core.agent.OperatorManager: td>: create_empty_table_udp.sql

2022-04-30 07:00:07.529 +0000 [INFO] (0252@[1:tbl1:76144781:411862721]+create_table_customers) io.digdag.standards.operator.td.TdOperatorFactory$TdOperator: Started presto job id=1372904946:
DROP TABLE IF EXISTS tmp_customers;
CREATE TABLE tmp_customers (customer_id VARCHAR)
  WITH (bucketed_on = array['customer_id'], bucket_count = 512);


2022-04-30 07:00:11.215 +0000 [INFO] (0420@[1:tbl1:76144781:411862721]+customers) io.digdag.core.agent.OperatorManager: td>: 

2022-04-30 07:00:12.138 +0000 [INFO] (0634@[1:tbl1:76144781:411862721]+customers) io.digdag.standards.operator.td.TdOperatorFactory$TdOperator: Started hive job id=1372905245:
INSERT INTO TABLE `tmp_customers`
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m"""  # noqa

    expected_sql = """CREATE DATABASE tbl1;
ALTER TABLE tbl1.cdp_tmp_behavior_behavior_1 RENAME TO tbl1.behavior_behavior_1;
DROP TABLE IF EXISTS tmp_customers;
CREATE TABLE tmp_customers (customer_id VARCHAR)
  WITH (bucketed_on = array['customer_id'], bucket_count = 512)
;
INSERT INTO TABLE `tmp_customers`
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m
;"""

    assert extract_sql(log) == expected_sql


def test_extractg_sql_with_comment():
    log = """2020-11-11 01:29:29.949 +0000 [INFO] (0538@[10778:db1]+customers) io.digdag.core.agent.OperatorManager: td>: 
2020-11-11 01:29:30.489 +0000 [INFO] (0538@[10778:db1]+customers) io.digdag.standards.operator.td.TdOperatorFactory$TdOperator: Started presto job id=884667004:
-- project_name: db1
-- workflow_name: audience
-- task_name: +customers
INSERT INTO "tmp_customers"
-- workflow task: +customers
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m
-- set session join_distribution_type = 'PARTITIONED'"""  # noqa

    expected_sql = """-- project_name: db1
-- workflow_name: audience
-- task_name: +customers
INSERT INTO "tmp_customers"
-- workflow task: +customers
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m
-- set session join_distribution_type = 'PARTITIONED'
;"""  # noqa

    assert extract_sql(log) == expected_sql


def test_extract_td_sql():
    log = """2022-04-30 07:00:04.079 +0000 [INFO] (0184@[1:tbl1:76144781:411862721]+create_database) io.digdag.core.agent.OperatorManager: td_ddl>: 
2022-04-30 07:00:04.153 +0000 [INFO] (0184@[1:tbl1:76144781:411862721]+create_database) io.digdag.standards.operator.td.TdDdlOperatorFactory$TdDdlOperator: Creating TD database tbl1

2022-04-30 07:04:38.245 +0000 [INFO] (0351@[1:tbl1:76144781:411862721]+rename) io.digdag.core.agent.OperatorManager: td_ddl>: 
2022-04-30 07:04:38.582 +0000 [INFO] (0351@[1:tbl1:76144781:411862721]+rename) io.digdag.standards.operator.td.TdDdlOperatorFactory$TdDdlOperator: Renaming TD table tbl1.cdp_tmp_behavior_behavior_1 -> behavior_behavior_1

2022-04-30 07:00:05.910 +0000 [INFO] (0222@[1:tbl1:76144781:411862721]+create_table_customers) io.digdag.core.agent.OperatorManager: td>: create_empty_table_udp.sql

2022-04-30 07:00:07.529 +0000 [INFO] (0252@[1:tbl1:76144781:411862721]+create_table_customers) io.digdag.standards.operator.td.TdOperatorFactory$TdOperator: Started presto job id=1372904946:
DROP TABLE IF EXISTS tmp_customers;
CREATE TABLE tmp_customers (customer_id VARCHAR)
  WITH (bucketed_on = array['customer_id'], bucket_count = 512);


2022-04-30 07:00:11.215 +0000 [INFO] (0420@[1:tbl1:76144781:411862721]+customers) io.digdag.core.agent.OperatorManager: td>: 

2022-04-30 07:00:12.138 +0000 [INFO] (0634@[1:tbl1:76144781:411862721]+customers) io.digdag.standards.operator.td.TdOperatorFactory$TdOperator: Started hive job id=1372905245:
INSERT INTO TABLE `tmp_customers`
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m"""  # noqa

    expected_output = """2022-04-30 07:00:04.079 +0000 [INFO] (0184@[1:tbl1:76144781:411862721]+create_database) io.digdag.core.agent.OperatorManager: td_ddl>: 
CREATE DATABASE tbl1;

2022-04-30 07:04:38.245 +0000 [INFO] (0351@[1:tbl1:76144781:411862721]+rename) io.digdag.core.agent.OperatorManager: td_ddl>: 
ALTER TABLE tbl1.cdp_tmp_behavior_behavior_1 RENAME TO tbl1.behavior_behavior_1;

2022-04-30 07:00:05.910 +0000 [INFO] (0222@[1:tbl1:76144781:411862721]+create_table_customers) io.digdag.core.agent.OperatorManager: td>: create_empty_table_udp.sql

DROP TABLE IF EXISTS tmp_customers;
CREATE TABLE tmp_customers (customer_id VARCHAR)
  WITH (bucketed_on = array['customer_id'], bucket_count = 512)
;


2022-04-30 07:00:11.215 +0000 [INFO] (0420@[1:tbl1:76144781:411862721]+customers) io.digdag.core.agent.OperatorManager: td>: 

INSERT INTO TABLE `tmp_customers`
select
    m.customer_id,
    m.`td_client_id`,
    m.`email`
from (
    select
      customer_id,
      td_last(`td_client_id`, time) as `td_client_id`,
      td_last(`email`, time) as `email`
    from `source_tbl`.`users`
    group by 1
  ) m
;"""  # noqa

    assert extract_td_sql(log) == expected_output
