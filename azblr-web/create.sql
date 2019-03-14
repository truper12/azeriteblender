CREATE TABLE `m_class` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `name_en` VARCHAR(45) NOT NULL,
  `color` VARCHAR(45) NOT NULL
  PRIMARY KEY (`id`));

INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('1', '전사', 'warrior', '#C79C6E');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('2', '성기사', 'paladin', '#F58CBA');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('3', '사냥꾼', 'hunter', '#ABD473');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('4', '도적', 'rogue', '#FFF569');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('5', '사제', 'priest', '#FFFFFF');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('6', '죽음의 기사', 'death_knight', '#C41F3B');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('7', '주술사', 'shaman', '#0070DE');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('8', '마법사', 'mage', '#40C7EB');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('9', '흑마법사', 'warlock', '#8787ED');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('10', '수도사', 'monk', '#00FF96');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('11', '드루이드', 'druid', '#FF7D0A');
INSERT INTO `m_class` (`id`, `name`, `name_en`, `color`) VALUES ('12', '악마사냥꾼', 'demon_hunter', '#A330C9');


CREATE TABLE `m_class_specialization` (
  `id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `name_en` VARCHAR(45) NOT NULL,
  `available` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_mcs_class_id_idx` (`class_id` ASC),
  CONSTRAINT `fk_mcs_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `m_class` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT);

INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('71', '1', '무기', 'arms', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('72', '1', '분노', 'fury', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('73', '1', '방어', 'protection', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('65', '2', '신성', 'holy', '0');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('66', '2', '보호', 'protection', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('70', '2', '징벌', 'retribution', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('253', '3', '야수', 'beast_mastery', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('254', '3', '사격', 'marksmanship', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('255', '3', '생존', 'survival', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('259', '4', '암살', 'assassination', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('260', '4', '무법', 'outlaw', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('261', '4', '잠행', 'subtlety', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('256', '5', '수양', 'discipline', '0');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('257', '5', '신성', 'holy', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('258', '5', '암흑', 'shadow', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('250', '6', '혈기', 'blood', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('251', '6', '냉기', 'frost', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('252', '6', '부정', 'unholy', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('262', '7', '정기', 'elemental', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('263', '7', '고양', 'enhancement', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('264', '7', '복원', 'restoration', '0');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('62', '8', '비전', 'arcane', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('63', '8', '화염', 'fire', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('64', '8', '냉기', 'frost', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('265', '9', '고통', 'affliction', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('266', '9', '악마', 'demonology', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('267', '9', '파괴', 'destruction', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('268', '10', '양조', 'brewmaster', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('269', '10', '풍운', 'windwalker', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('270', '10', '운무', 'mistweaver', '0');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('102', '11', '조화', 'balance', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('103', '11', '야성', 'feral', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('104', '11', '수호', 'guardian', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('105', '11', '회복', 'restoration', '0');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('577', '12', '파멸', 'havoc', '1');
INSERT INTO `m_class_specialization` (`id`, `class_id`, `name`, `name_en`, `available`) VALUES ('581', '12', '복수', 'vengeance', '1');


CREATE TABLE `m_inventory_type` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `slot_to` INT NOT NULL,
  PRIMARY KEY (`id`));

INSERT INTO `m_inventory_type` (`id`, `name`, `slot_to`) VALUES ('1', '머리', `1`);
INSERT INTO `m_inventory_type` (`id`, `name`, `slot_to`) VALUES ('3', '어깨', `3`);
INSERT INTO `m_inventory_type` (`id`, `name`, `slot_to`) VALUES ('5', '가슴', `5`);
INSERT INTO `m_inventory_type` (`id`, `name`, `slot_to`) VALUES ('5', '로브(가슴)', `5`);

CREATE TABLE `m_fight_style` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `name_en` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

INSERT INTO `m_fight_style` (`id`, `name`, `name_en`) VALUES ('1', '단일 타겟', 'patchwerk');
INSERT INTO `m_fight_style` (`id`, `name`, `name_en`) VALUES ('2', '다중 타겟', 'hecticaddcleave');


CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login_id` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `token` VARCHAR(255) NULL,
  `last_login` DATETIME NULL,
  `created_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique` (`login_id` ASC));

CREATE TABLE `user_class` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `specialization_id` INT NOT NULL,
  `updated_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_uc_user_id_idx` (`user_id` ASC),
  INDEX `fk_uc_class_id_idx` (`class_id` ASC),
  INDEX `fk_uc_specialization_id_idx` (`specialization_id` ASC),
  UNIQUE INDEX `unique` (`user_id` ASC, `class_id` ASC, `specialization_id` ASC),
  CONSTRAINT `fk_uc_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_uc_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `m_class` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_uc_specialization_id`
    FOREIGN KEY (`specialization_id`)
    REFERENCES `m_class_specialization` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT);

CREATE TABLE `user_class_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_class_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `created_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_uci_user_class_id_idx` (`user_class_id` ASC),
  CONSTRAINT `fk_uci_user_class_id`
    FOREIGN KEY (`user_class_id`)
    REFERENCES `user_class` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT);

CREATE TABLE `crawler` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `class_id` INT NOT NULL,
  `specialization_id` INT NOT NULL,
  `fight_style_id` INT NOT NULL,
  `updated_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_crawler_class_id_idx` (`class_id` ASC),
  INDEX `fk_crawler_specialization_id_idx` (`specialization_id` ASC),
  INDEX `fk_crawler_fight_style_id_idx` (`fight_style_id` ASC),
  UNIQUE INDEX `unique` (`class_id` ASC, `specialization_id` ASC, `fight_style_id` ASC),
  CONSTRAINT `fk_crawler_class_id`
    FOREIGN KEY (`class_id`)
    REFERENCES `m_class` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_crawler_specialization_id`
    FOREIGN KEY (`specialization_id`)
    REFERENCES `m_class_specialization` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_crawler_fight_style_id`
    FOREIGN KEY (`fight_style_id`)
    REFERENCES `m_fight_style` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT);

CREATE TABLE `crawler_score` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `crawler_id` INT NOT NULL,
  `spell_id` INT NOT NULL,
  `sub_spell_name` VARCHAR(45) NOT NULL,
  `sub_spell_id` VARCHAR(45) NULL,
  `count` INT NOT NULL,
  `item_level` INT NOT NULL,
  `score` INT NOT NULL,
  `created_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_cs_crawler_id_idx` (`crawler_id` ASC),
  UNIQUE INDEX `unique` (`crawler_id` ASC, `spell_id` ASC, `sub_spell_name` ASC, `count` ASC, `item_level` ASC),
  CONSTRAINT `fk_cs_crawler_id`
    FOREIGN KEY (`crawler_id`)
    REFERENCES `crawler` (`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT);
