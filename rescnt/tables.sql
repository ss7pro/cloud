
--
-- resources
--
-- network interface counters on vm
-- 'type':'interface','value':'net0','parent':'instance_resource_id'
-- disk counter on vm
-- 'type':'disk','value':'vda','parent':'instance_resource_id'
-- ip address traffic counter on default gateway (external traffic)
-- 'type':'ipextr','value':'178.239.140.10'
-- ip address traffic counter on default gateway (internal traffic)
-- 'type':'ipintr','value':'178.239.140.10'
--
-- counters
--
-- disk
--
-- 'type':'rrq' - read requests
-- 'type':'wrq' - read requests
-- 'type':'rdb' - read bytes
-- 'type':'wrb' - write bytes
--
-- network traffic
--
-- 'type':'bin' - bytes in
-- 'type':'bout' - bytes out



CREATE TABLE resources (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent  BIGINT UNSIGNED,
    type VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    zone VARCHAR(255) NOT NULL,
    added TIMESTAMP,
    INDEX (type,value,zone),
    INDEX (type,parent)
) ENGINE=INNODB;


CREATE TABLE counters (
    resource BIGINT UNSIGNED NOT NULL,
    type VARCHAR(255) NOT NULL,
    value BIGINT UNSIGNED,
    delta BIGINT UNSIGNED,
    added DATETIME NOT NULL,
    prev DATETIME,
    INDEX (resource,type,added),
    INDEX (resource,type),
    FOREIGN KEY (resource) REFERENCES resources(id) ON DELETE RESTRICT
) ENGINE=INNODB;
