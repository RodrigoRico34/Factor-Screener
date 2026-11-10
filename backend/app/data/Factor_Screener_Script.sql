-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema factor_screener
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema factor_screener
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `factor_screener` DEFAULT CHARACTER SET utf8 ;
USE `factor_screener` ;

-- -----------------------------------------------------
-- Table `factor_screener`.`stocks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `factor_screener`.`stocks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ticker` VARCHAR(10) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `sector` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ticker_UNIQUE` (`ticker` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `factor_screener`.`prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `factor_screener`.`prices` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `close` DECIMAL(12,4) NOT NULL,
  `stocks_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_prices_stocks_idx` (`stocks_id` ASC) VISIBLE,
  UNIQUE INDEX `uq_prices_stock_date` (`stocks_id` ASC, `date` ASC) VISIBLE,
  CONSTRAINT `fk_prices_stocks`
    FOREIGN KEY (`stocks_id`)
    REFERENCES `factor_screener`.`stocks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `factor_screener`.`factors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `factor_screener`.`factors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `momentum_1m` DOUBLE NULL,
  `momentum_3m` DOUBLE NULL,
  `momentum_6m` DOUBLE NULL,
  `momentum_12m` DOUBLE NULL,
  `decile` INT NULL,
  `stocks_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_factors_stocks1_idx` (`stocks_id` ASC) VISIBLE,
  UNIQUE INDEX `uq_factors_stock_date` (`stocks_id` ASC, `date` ASC) VISIBLE,
  CONSTRAINT `chk_decile` CHECK (`decile` BETWEEN 1 AND 10),
  CONSTRAINT `fk_factors_stocks1`
    FOREIGN KEY (`stocks_id`)
    REFERENCES `factor_screener`.`stocks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
