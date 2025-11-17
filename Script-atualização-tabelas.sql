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

delimiter $$
create procedure cadGestor_telefone(
    IN p_cpf VARCHAR(14),
    IN p_nome VARCHAR(60),
    IN p_email VARCHAR(80),
    IN p_senha_hash VARCHAR(128),
    IN p_usuario VARCHAR(20),
    IN p_telefone VARCHAR(15))
    begin
        INSERT INTO Gestor (CPF, nome, email, senha_hash, usuario)
			VALUES (p_cpf, p_nome, p_email, p_senha_hash, p_usuario);
            
		IF p_telefone IS NOT NULL AND p_telefone <> ''
			THEN INSERT INTO Telefone (numero, Gestor_CPF)
				VALUES (p_telefone, p_cpf);
    END IF;

    end$$
delimiter;
    

    


delimiter $$

CREATE PROCEDURE cadCooperativa_tel_endereco(
    IN p_cnpj             VARCHAR(18),
    IN p_razaoSocial      VARCHAR(60),
    IN p_nomeResponsavel  VARCHAR(60),
    IN p_cpfResponsavel   VARCHAR(14),
    IN p_emailInst        VARCHAR(80),
    IN p_senha_hash       VARCHAR(128),
    IN p_usuario          VARCHAR(20),
    IN p_telefone         VARCHAR(15),

    IN p_uf               CHAR(2),
    IN p_cidade           VARCHAR(45),
    IN p_bairro           VARCHAR(45),
    IN p_rua              VARCHAR(45),
    IN p_numero           INT,
    IN p_comp             VARCHAR(45),
    IN p_cep              VARCHAR(9)
)
BEGIN
    DECLARE v_idEnd INT;

    
    INSERT INTO Endereco (UF, cidade, bairro, rua, numero, comp, cep)
    VALUES (p_uf, p_cidade, p_bairro, p_rua, p_numero, p_comp, p_cep);

    
    SET v_idEnd = LAST_INSERT_ID();

    
    INSERT INTO Cooperativa (
        CNPJ,
        razaoSocial,
        nomeResponsavel,
        cpfResponsavel,
        emailInstitucional,
        senha_hash,
        usuario,
        Endereco_idEndereco
    )
    VALUES (
        p_cnpj,
        p_razaoSocial,
        p_nomeResponsavel,
        p_cpfResponsavel,
        p_emailInst,
        p_senha_hash,
        p_usuario,
        v_idEnd
    );

    
    IF p_telefone IS NOT NULL AND p_telefone <> '' THEN
        INSERT INTO Telefone (numero, Cooperativa_CNPJ)
        VALUES (p_telefone, p_cnpj);
    END IF;
END$$

delimiter ;