create or replace package body amazon_aws_auth_pkg
as

  

  g_aws_id                 varchar2(20) := 'my_aws_id'; 
  g_aws_key                varchar2(40) := 'my_aws_key'; 

  g_gmt_offset             number := null; 


function get_auth_string (p_string in varchar2) return varchar2
as
 l_returnvalue      varchar2(32000);
 l_encrypted_raw    raw (2000);             
 l_decrypted_raw    raw (2000);             
 l_key_bytes_raw    raw (64);               
begin

  

  l_key_bytes_raw := utl_i18n.string_to_raw (g_aws_key,  'al32utf8');
  l_decrypted_raw := utl_i18n.string_to_raw (p_string, 'al32utf8');

  l_encrypted_raw := dbms_crypto.mac (src => l_decrypted_raw, typ => dbms_crypto.hmac_sh1, key => l_key_bytes_raw);

  l_returnvalue := utl_i18n.raw_to_char (utl_encode.base64_encode(l_encrypted_raw), 'al32utf8');

  l_returnvalue := 'aws ' || g_aws_id || ':' || l_returnvalue;

  return l_returnvalue;

end get_auth_string;


function get_signature (p_string in varchar2) return varchar2
as

begin

  

  return substr(get_auth_string(p_string),26);

end get_signature;


function get_aws_id return varchar2
as
begin

  

  return g_aws_id;

end get_aws_id;


function get_date_string (p_date in date := sysdate) return varchar2
as
  l_returnvalue varchar2(255);
  l_date_as_time timestamp(6);
  l_time_utc timestamp(6);
begin

  

  if g_gmt_offset is null then
    l_date_as_time := cast(p_date as timestamp);
    l_time_utc := sys_extract_utc(l_date_as_time);
    l_returnvalue := to_char(l_time_utc, 'dy, dd mon yyyy hh24:mi:ss', 'nls_date_language = american') || ' gmt';
  else
    l_returnvalue := to_char(p_date + g_gmt_offset/24, 'dy, dd mon yyyy hh24:mi:ss', 'nls_date_language = american') || ' gmt';
  end if;

  return l_returnvalue;

end get_date_string;


function get_epoch (p_date in date) return number
as
  l_returnvalue number;
begin

  

  l_returnvalue := trunc((p_date - to_date('01-01-1970','mm-dd-yyyy')) * 24 * 60 * 60);

  return l_returnvalue;

end get_epoch;


procedure set_aws_id (p_aws_id in varchar2)
as
begin

  

  g_aws_id := p_aws_id;


end set_aws_id;


procedure set_aws_key (p_aws_key in varchar2)
as
begin

  

  g_aws_key := p_aws_key;

end set_aws_key;


procedure set_gmt_offset (p_gmt_offset in number)
as
begin

  

  g_gmt_offset := p_gmt_offset;

end set_gmt_offset;


procedure init (p_aws_id in varchar2,
                p_aws_key in varchar2,
                p_gmt_offset in number := null)
as
begin

  

  g_aws_id := p_aws_id;
  g_aws_key := p_aws_key;
  g_gmt_offset := p_gmt_offset;

end init;

end amazon_aws_auth_pkg;
/
