-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema scoreboard_tennis
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema scoreboard_tennis
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `scoreboard_tennis` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema scoreboard_tennis
-- -----------------------------------------------------
USE `scoreboard_tennis` ;

-- -----------------------------------------------------
-- Table `scoreboard_tennis`.`player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoreboard_tennis`.`player` (
  `player_id` INT NOT NULL AUTO_INCREMENT,
  `player_name` VARCHAR(200) NULL,
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scoreboard_tennis`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoreboard_tennis`.`team` (
  `team_id` INT NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(45) NULL,
  PRIMARY KEY (`team_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scoreboard_tennis`.`match`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoreboard_tennis`.`match` (
  `match_id` INT NOT NULL,
  `number_of_sets` VARCHAR(50) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `is_tiebreak` TINYINT NULL,
  PRIMARY KEY (`match_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scoreboard_tennis`.`player_has_team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoreboard_tennis`.`player_has_team` (
  `player_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  PRIMARY KEY (`player_id`, `team_id`),
  INDEX `fk_player_has_team_team1_idx` (`team_id` ASC) VISIBLE,
  INDEX `fk_player_has_team_player_idx` (`player_id` ASC) VISIBLE,
  CONSTRAINT `fk_player_has_team_player`
    FOREIGN KEY (`player_id`)
    REFERENCES `scoreboard_tennis`.`player` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_has_team_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `scoreboard_tennis`.`team` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scoreboard_tennis`.`team_has_match`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scoreboard_tennis`.`team_has_match` (
  `team_id` INT NOT NULL,
  `match_id` INT NOT NULL,
  `team_points` INT NULL,
  PRIMARY KEY (`team_id`, `match_id`),
  INDEX `fk_team_has_match_match1_idx` (`match_id` ASC) VISIBLE,
  INDEX `fk_team_has_match_team1_idx` (`team_id` ASC) VISIBLE,
  CONSTRAINT `fk_team_has_match_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `scoreboard_tennis`.`team` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_team_has_match_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `scoreboard_tennis`.`match` (`match_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
