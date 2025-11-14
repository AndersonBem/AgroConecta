ALTER TABLE `Gestor`
  ADD COLUMN `senha_hash` VARCHAR(128) NOT NULL AFTER `email`;
  
ALTER TABLE `OperadorArmazem`
  ADD COLUMN `senha_hash` VARCHAR(128) NOT NULL AFTER `email`;

ALTER TABLE `Cooperativa`
  ADD COLUMN `senha_hash` VARCHAR(128) NOT NULL AFTER `emailInstitucional`;
  
ALTER TABLE `Gestor`
  ADD COLUMN `usuario` VARCHAR(20) NOT NULL AFTER `senha_hash`;
  
ALTER TABLE `OperadorArmazem`
  ADD COLUMN `usuario` VARCHAR(20) NOT NULL AFTER `senha_hash`;
  
ALTER TABLE `Cooperativa`
  ADD COLUMN `usuario` VARCHAR(20) NOT NULL AFTER `senha_hash`;
