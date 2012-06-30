
CREATE TABLE ChargePeriods (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    begin DATETIME NOT NULL,
    end DATETIME NOT NULL,
    UNIQUE INDEX(begin,end)
) ENGINE=INNODB;

CREATE TABLE Tenants (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    balance DOUBLE(32,8) NOT NULL
) ENGINE=INNODB;

CREATE TABLE RateGroups (
    GroupName VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    units BIGINT UNSIGNED DEFAULT NULL,
    rate DOUBLE PRECISION(32,8) NOT NULL,
    frequency BIGINT UNSIGNED NOT NULL,
    minunits BIGINT UNSIGNED DEFAULT NULL,
    ValidFrom DATETIME NOT NULL,
    ValidTo DATETIME DEFAULT NULL,
    INDEX (GroupName,minunits,ValidFrom,ValidTo)
) ENGINE=INNODB;

CREATE TABLE ResourceChargeSchemas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) DEFAULT NULL,
    area VARCHAR(255) DEFAULT NULL,
    RateGroupName VARCHAR(255) NOT NULL,
    INDEX (name),
    FOREIGN KEY (RateGroupName) REFERENCES RateGroups(GroupName) ON DELETE RESTRICT
) ENGINE=INNODB;

CREATE TABLE ResourceTypes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    zone VARCHAR(255) NOT NULL,
    ChargeSchemaName VARCHAR(255) NOT NULL,
    INDEX (name,type,zone),
    FOREIGN KEY (ChargeSchemaName) REFERENCES ResourceChargeSchemas(name) ON DELETE RESTRICT
) ENGINE=INNODB;


CREATE TABLE Services (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tenant VARCHAR(36) NOT NULL,
    ResourceType BIGINT UNSIGNED NOT NULL,
    ResourceId VARCHAR(255) NOT NULL,
    created DATETIME NOT NULL,
    dropped DATETIME DEFAULT NULL,
    INDEX (created,dropped),
    INDEX (ResourceId),
    UNIQUE INDEX (ResourceType,ResourceId),
    FOREIGN KEY (tenant) REFERENCES Tenants(id) ON DELETE RESTRICT,
    FOREIGN KEY (ResourceType) REFERENCES ResourceTypes(id) ON DELETE RESTRICT
) ENGINE=INNODB;


CREATE TABLE ChargeQueue (
    service BIGINT UNSIGNED NOT NULL,
    ResourceChargeSchema BIGINT UNSIGNED NOT NULL,
    NextCharge DATETIME NOT NULL,
    NextRun DATETIME DEFAULT NULL,
    LastRun DATETIME DEFAULT '1970-01-01 01:00:00',
    LastCounter DATETIME DEFAULT NULL,
    LastCharge DATETIME DEFAULT NULL,
    status VARCHAR(255) DEFAULT NULL,
    SavedUnits DOUBLE PRECISION(32,8) DEFAULT 0.0000000 NOT NULL,
    PRIMARY KEY (service,ResourceChargeSchema),
    INDEX (NextRun,status),
    FOREIGN KEY (service) REFERENCES Services(id) ON DELETE RESTRICT,
    FOREIGN KEY (ResourceChargeSchema) REFERENCES ResourceChargeSchemas(id) ON DELETE RESTRICT
) ENGINE=INNODB;

CREATE TABLE ServiceEvents (
    service BIGINT UNSIGNED NOT NULL,
    ResourceChargeSchema BIGINT UNSIGNED DEFAULT NULL,
    ts DATETIME NOT NULL,
    event VARCHAR(32) NOT NULL,
    size BIGINT UNSIGNED NOT NULL,
    INDEX (service,ResourceChargeSchema),
    INDEX (service,ResourceChargeSchema,ts),
    FOREIGN KEY (service) REFERENCES Services(id) ON DELETE RESTRICT,
    FOREIGN KEY (ResourceChargeSchema) REFERENCES ResourceChargeSchemas(id) ON DELETE RESTRICT
) ENGINE=INNODB;

CREATE TABLE ResourcePeriodCharges (
    service BIGINT UNSIGNED NOT NULL,
    ResourceChargeSchema BIGINT UNSIGNED NOT NULL,
    amount DOUBLE PRECISION(32,8) NOT NULL,
    units BIGINT UNSIGNED DEFAULT NULL,
    RunTime DATETIME NOT NULL,
    ChargeTime DATETIME NOT NULL,
    INDEX (service,ResourceChargeSchema,ChargeTime),
    INDEX (service,ResourceChargeSchema),
    INDEX (service,ChargeTime),
    FOREIGN KEY (service) REFERENCES Services(id) ON DELETE RESTRICT,
    FOREIGN KEY (ResourceChargeSchema) REFERENCES ResourceChargeSchemas(id) ON DELETE RESTRICT
) ENGINE=INNODB;


CREATE OR REPLACE VIEW ChargeQueueView AS SELECT
                                    s.id as ServiceId,
                                    s.tenant as TenantId,
                                    s.created as ServiceCreated,
                                    s.dropped as ServiceDropped,
                                    s.ResourceId as ResourceId,
                                    cq.NextCharge as NextCharge,
                                    cq.NextRun as NextRun,
                                    cq.LastRun as LastRun,
                                    cq.status as Status,
                                    cq.SavedUnits as SavedUnits,
                                    cq.LastCharge as LastCharge,
                                    cq.LastCounter as LastCounter,
                                    rcs.id as ResourceChargeSchemaId,
                                    rcs.name as ResourceChargeSchemaName,
                                    rcs.type as ResourceChargeSchemaType,
                                    rcs.area as ResourceChargeSchemaArea,
                                    rcs.RateGroupName as RateGroupName
                                    FROM
                                    ChargeQueue as cq LEFT JOIN
                                    Services AS s ON
                                    cq.service = s.id LEFT JOIN
                                    ResourceChargeSchemas AS rcs ON
                                    cq.ResourceChargeSchema = rcs.id;

CREATE OR REPLACE VIEW ServiceTypeView AS SELECT
                                    s.id AS ServiceId,
                                    s.tenant AS TenantId,
                                    s.ResourceId AS ResourceId,
                                    s.created AS ServiceCreated,
                                    s.dropped AS ServiceDropped,
                                    r.name AS ResourceName,
                                    r.type AS ResourceType,
                                    r.zone AS ResourceZone,
                                    r.ChargeSchemaName AS
                                        ResourceChargeSchemaName
                                    FROM Services AS s LEFT JOIN
                                    ResourceTypes AS r ON
                                    s.ResourceType = r.id;
