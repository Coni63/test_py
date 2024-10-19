-- Create a test table
CREATE TABLE test_table (
    id NUMBER,
    name VARCHAR2(50)
);

-- Function that updates the test_table
CREATE OR REPLACE FUNCTION update_test_table_func(p_id NUMBER, p_name VARCHAR2) RETURN VARCHAR2 IS
BEGIN
    UPDATE test_table
    SET name = p_name
    WHERE id = p_id;

    -- Check if the update succeeded
    IF SQL%ROWCOUNT = 0 THEN
        -- If no row was updated, insert a new row
        INSERT INTO test_table (id, name)
        VALUES (p_id, p_name);
    END IF;

    RETURN 'Table updated successfully';
END;
/

-- Procedure B, which calls the function to update the table
CREATE OR REPLACE PROCEDURE proc_B IS
    result VARCHAR2(100);
BEGIN
    -- Call the function to update test_table
    result := update_test_table_func(1, 'Updated Name');
    DBMS_OUTPUT.PUT_LINE(result);
END;
/

-- Procedure A, which calls Procedure B
CREATE OR REPLACE PROCEDURE proc_A IS
BEGIN
    -- Call proc_B
    proc_B;
    DBMS_OUTPUT.PUT_LINE('proc_A finished');
END;
/

-- Run proc_A to test the dependencies
BEGIN
    proc_A;
END;
/