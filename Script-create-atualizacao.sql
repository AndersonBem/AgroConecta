-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema AgroConecta
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema AgroConecta
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `AgroConecta` DEFAULT CHARACTER SET utf8 ;
USE `AgroConecta` ;

-- -----------------------------------------------------
-- Table `AgroConecta`.`Gestor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Gestor` (
  `CPF` VARCHAR(14) NOT NULL,
  `nome` VARCHAR(60) NOT NULL,
  `email` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Endereco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Endereco` (
  `idEndereco` INT NOT NULL AUTO_INCREMENT,
  `UF` CHAR(2) NOT NULL,
  `cidade` VARCHAR(45) NOT NULL,
  `bairro` VARCHAR(45) NOT NULL,
  `rua` VARCHAR(45) NOT NULL,
  `numero` INT NOT NULL,
  `comp` VARCHAR(45) NULL,
  `cep` VARCHAR(9) NOT NULL,
  PRIMARY KEY (`idEndereco`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`OperadorArmazem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`OperadorArmazem` (
  `idOperadorArmazem` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(60) NOT NULL,
  `email` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`idOperadorArmazem`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Armazem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Armazem` (
  `idArmazem` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(60) NOT NULL,
  `descricao` VARCHAR(150) NULL,
  `Gestor_CPF` VARCHAR(14) NOT NULL,
  `Endereco_idEndereco` INT NOT NULL,
  `OperadorArmazem_idOperadorArmazem` INT NULL,
  PRIMARY KEY (`idArmazem`),
  INDEX `fk_Armazem_Gestor_idx` (`Gestor_CPF` ASC) VISIBLE,
  INDEX `fk_Armazem_Endereco1_idx` (`Endereco_idEndereco` ASC) VISIBLE,
  INDEX `fk_Armazem_OperadorArmazem1_idx` (`OperadorArmazem_idOperadorArmazem` ASC) VISIBLE,
  CONSTRAINT `fk_Armazem_Gestor`
    FOREIGN KEY (`Gestor_CPF`)
    REFERENCES `AgroConecta`.`Gestor` (`CPF`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Armazem_Endereco1`
    FOREIGN KEY (`Endereco_idEndereco`)
    REFERENCES `AgroConecta`.`Endereco` (`idEndereco`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Armazem_OperadorArmazem1`
    FOREIGN KEY (`OperadorArmazem_idOperadorArmazem`)
    REFERENCES `AgroConecta`.`OperadorArmazem` (`idOperadorArmazem`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Cooperativa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Cooperativa` (
  `CNPJ` VARCHAR(18) NOT NULL,
  `razaoSocial` VARCHAR(60) NOT NULL,
  `nomeResponsavel` VARCHAR(60) NOT NULL,
  `cpfResponsavel` VARCHAR(14) NULL,
  `emailInstitucional` VARCHAR(80) NOT NULL,
  `Endereco_idEndereco` INT NOT NULL,
  PRIMARY KEY (`CNPJ`),
  UNIQUE INDEX `emailInstitucional_UNIQUE` (`emailInstitucional` ASC) VISIBLE,
  INDEX `fk_Cooperativa_Endereco1_idx` (`Endereco_idEndereco` ASC) VISIBLE,
  CONSTRAINT `fk_Cooperativa_Endereco1`
    FOREIGN KEY (`Endereco_idEndereco`)
    REFERENCES `AgroConecta`.`Endereco` (`idEndereco`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Telefone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Telefone` (
  `idTelefone` INT NOT NULL AUTO_INCREMENT,
  `numero` VARCHAR(15) NULL,
  `Gestor_CPF` VARCHAR(14) NULL,
  `Cooperativa_CNPJ` VARCHAR(18) NULL,
  PRIMARY KEY (`idTelefone`),
  INDEX `fk_Telefone_Gestor1_idx` (`Gestor_CPF` ASC) VISIBLE,
  INDEX `fk_Telefone_Cooperativa1_idx` (`Cooperativa_CNPJ` ASC) VISIBLE,
  CONSTRAINT `fk_Telefone_Gestor1`
    FOREIGN KEY (`Gestor_CPF`)
    REFERENCES `AgroConecta`.`Gestor` (`CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Telefone_Cooperativa1`
    FOREIGN KEY (`Cooperativa_CNPJ`)
    REFERENCES `AgroConecta`.`Cooperativa` (`CNPJ`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`TipoSemente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`TipoSemente` (
  `idTipoSemente` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `descricao` VARCHAR(150) NULL,
  PRIMARY KEY (`idTipoSemente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Lote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Lote` (
  `idLote` INT NOT NULL AUTO_INCREMENT,
  `dataEntrada` DATE NOT NULL,
  `dataVencimento` DATE NOT NULL,
  `dataSaida` DATETIME NULL,
  `peso` INT UNSIGNED NOT NULL,
  `Armazem_idArmazem` INT NOT NULL,
  `TipoSemente_idTipoSemente` INT NOT NULL,
  `qr_payload` VARCHAR(255) NULL,
  `Lotecol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idLote`),
  INDEX `fk_Lote_Armazem1_idx` (`Armazem_idArmazem` ASC) VISIBLE,
  INDEX `fk_Lote_TipoSemente1_idx` (`TipoSemente_idTipoSemente` ASC) VISIBLE,
  CONSTRAINT `fk_Lote_Armazem1`
    FOREIGN KEY (`Armazem_idArmazem`)
    REFERENCES `AgroConecta`.`Armazem` (`idArmazem`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Lote_TipoSemente1`
    FOREIGN KEY (`TipoSemente_idTipoSemente`)
    REFERENCES `AgroConecta`.`TipoSemente` (`idTipoSemente`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Safra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Safra` (
  `idSafra` INT NOT NULL AUTO_INCREMENT,
  `ano` DATE NOT NULL,
  `descricao` VARCHAR(150) NULL,
  `Safracol` VARCHAR(45) NULL,
  PRIMARY KEY (`idSafra`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Status` (
  `idStatus` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `descricao` VARCHAR(150) NULL,
  PRIMARY KEY (`idStatus`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`Solicitacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`Solicitacao` (
  `idSolicitacao` INT NOT NULL AUTO_INCREMENT,
  `quantidade` INT UNSIGNED NOT NULL,
  `numeroProdutoresBeneficiados` INT UNSIGNED NOT NULL,
  `observacao` VARCHAR(150) NULL,
  `Cooperativa_CNPJ` VARCHAR(18) NOT NULL,
  `Safra_idSafra` INT NOT NULL,
  `Status_idStatus` INT NOT NULL,
  PRIMARY KEY (`idSolicitacao`),
  INDEX `fk_Solicitacao_Cooperativa1_idx` (`Cooperativa_CNPJ` ASC) VISIBLE,
  INDEX `fk_Solicitacao_Safra1_idx` (`Safra_idSafra` ASC) VISIBLE,
  INDEX `fk_Solicitacao_Status1_idx` (`Status_idStatus` ASC) VISIBLE,
  CONSTRAINT `fk_Solicitacao_Cooperativa1`
    FOREIGN KEY (`Cooperativa_CNPJ`)
    REFERENCES `AgroConecta`.`Cooperativa` (`CNPJ`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Solicitacao_Safra1`
    FOREIGN KEY (`Safra_idSafra`)
    REFERENCES `AgroConecta`.`Safra` (`idSafra`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Solicitacao_Status1`
    FOREIGN KEY (`Status_idStatus`)
    REFERENCES `AgroConecta`.`Status` (`idStatus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AgroConecta`.`SolicitacaoTipoSemente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AgroConecta`.`SolicitacaoTipoSemente` (
  `Solicitacao_idSolicitacao` INT NOT NULL,
  `TipoSemente_idTipoSemente` INT NOT NULL,
  `quantidade` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`Solicitacao_idSolicitacao`, `TipoSemente_idTipoSemente`),
  INDEX `fk_Solicitacao_has_TipoSemente_TipoSemente1_idx` (`TipoSemente_idTipoSemente` ASC) VISIBLE,
  INDEX `fk_Solicitacao_has_TipoSemente_Solicitacao1_idx` (`Solicitacao_idSolicitacao` ASC) VISIBLE,
  CONSTRAINT `fk_Solicitacao_has_TipoSemente_Solicitacao1`
    FOREIGN KEY (`Solicitacao_idSolicitacao`)
    REFERENCES `AgroConecta`.`Solicitacao` (`idSolicitacao`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Solicitacao_has_TipoSemente_TipoSemente1`
    FOREIGN KEY (`TipoSemente_idTipoSemente`)
    REFERENCES `AgroConecta`.`TipoSemente` (`idTipoSemente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
