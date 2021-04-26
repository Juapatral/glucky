--crear tabla con archivos concatenados
CREATE TABLE EjercicioDos.notificacionesClicked (`ts` BIGINT,`eventName` VARCHAR(256),`profile.identity` BIGINT,`profile.objectId` DOUBLE,`profile.all_identities` VARCHAR(256),`profile.platform` VARCHAR(256),`profile.phone` BIGINT,`profile.name` VARCHAR(256),`profile.email` VARCHAR(256),`profile.push_token` VARCHAR(256),`deviceInfo.make` VARCHAR(256),`deviceInfo.model` VARCHAR(256),`deviceInfo.appVersion` VARCHAR(256),`deviceInfo.sdkVersion` BIGINT,`deviceInfo.osVersion` VARCHAR(256),`deviceInfo.browser` VARCHAR(256),`deviceInfo.dpi` BIGINT,`deviceInfo.dimensions.width` BIGINT,`deviceInfo.dimensions.height` BIGINT,`deviceInfo.dimensions.unit` VARCHAR(256),`controlGroupName` DOUBLE,`eventProps.CT Source` VARCHAR(256),`eventProps.wzrk_cts` DOUBLE,`eventProps.wzrk_push_amp` BOOLEAN,`eventProps.wzrk_ck` DOUBLE,`eventProps.wzrk_from` VARCHAR(256),`eventProps.UTM` DOUBLE,`eventProps.wzrk_bi_liquid` DOUBLE,`eventProps.wzrk_c2a` DOUBLE,`eventProps.wzrk_pid` VARCHAR(256),`eventProps.Campaign id` DOUBLE,`eventProps.Install` DOUBLE,`eventProps.CT App Version` VARCHAR(256),`eventProps.Campaign type` VARCHAR(256),`eventProps.wzrk_dl_liquid` DOUBLE,`eventProps.wzrk_acct_id` VARCHAR(256),`eventProps.wzrk_cid` VARCHAR(256),`eventProps.wzrk_dl` VARCHAR(256),`eventProps.wzrk_pivot` VARCHAR(256),`eventProps.wzrk_bi` BIGINT,`eventProps.wzrk_bc` DOUBLE,`eventProps.wzrk_rnv` BOOLEAN,`eventProps.wzrk_bc_liquid` DOUBLE,`eventProps.RAW_STRING` DOUBLE,`eventProps.wzrk_pn` BOOLEAN,`eventProps.wzrk_cid_liquid` DOUBLE,`eventProps.wzrk_id` VARCHAR(256),`eventProps.wzrk_nms_liquid` DOUBLE,`eventProps.wzrk_ttl` BIGINT,`eventProps.wzrk_dt` VARCHAR(256))
;

insert table
gcloud sql import csv my-data-base gs://glucky_parte2/notificacion_clicked.csv -d EjercicioDos --table=notificacionesClicked

--crear tablas de archivos

-- DimPersonas

-- borrar tabla
-- drop table if exists EjercicioDos.DimPersonas
-- ;

-- crear tabla DimPersonas
create table if not exists EjercicioDos.DimPersonas(
	`profile.identity` BIGINT,
	`profile.all_identities` VARCHAR(256),
	`profile.platform` VARCHAR(256),
	`profile.phone` BIGINT,
	`profile.name` VARCHAR(256),
	`profile.email` VARCHAR(256),
	`deviceInfo.make` VARCHAR(256)
);

-- insertar datos
insert into  EjercicioDos.DimPersonas 
SELECT `profile.identity`, `profile.all_identities`, `profile.platform`, 
`profile.phone`, `profile.name`, `profile.email`, `deviceInfo.make`
FROM EjercicioDos.notificacionesClicked
;

-- FactMetrics

-- borrar tabla
--drop table if exists EjercicioDos.FactMetrics
--;

-- crear tabla FactMetrics
create table if not exists EjercicioDos.FactMetrics(
	`deviceInfo.dpi` BIGINT,
	`deviceInfo.dimensions.width` BIGINT,
	`deviceInfo.dimensions.height` BIGINT,
	`profile.identity` BIGINT

);

-- insertar datos
insert into EjercicioDos.FactMetrics
SELECT
`deviceInfo.dpi`, `deviceInfo.dimensions.width`, 
`deviceInfo.dimensions.height`, `profile.identity`
FROM EjercicioDos.notificacionesClicked
;


-- DimSource

-- borrar tabla
drop table if exists EjercicioDos.DimSource
;

-- crear tabla DimSource
create table if not exists  EjercicioDos.DimSource(
	`eventProps.wzrk_pid` VARCHAR(256),
	`eventProps.wzrk_cid` VARCHAR(256),
	`eventProps.wzrk_dt` VARCHAR(256)
);

-- insertar datos
insert into EjercicioDos.DimSource 
SELECT
`eventProps.wzrk_pid`, `eventProps.wzrk_cid`, 
`eventProps.wzrk_dt`
FROM EjercicioDos.notificacionesClicked
;

-- eliminar tabla staging

drop table if exists EjercicioDos.notificacionesClicked
;