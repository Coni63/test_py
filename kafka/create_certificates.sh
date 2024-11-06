# Generate the CA certificate
keytool -genkey -keyalg RSA -alias ca -dname "CN=CA,OU=Example,O=Example,L=Example,S=Example,C=US" -ext "san=dns:ca" -keystore ca.keystore.jks -storepass password -keypass password -validity 3650

# Export the CA certificate
keytool -export -keystore ca.keystore.jks -file ca.crt -storepass password -alias ca

# Create the truststore
keytool -import -file ca.crt -alias ca -keystore truststore.jks -storepass password -noprompt

# Create the keystore for the Kafka broker
keytool -genkey -keyalg RSA -alias broker -dname "CN=broker,OU=Example,O=Example,L=Example,S=Example,C=US" -ext "san=dns:broker" -keystore keystore.jks -storepass password -keypass password -validity 3650

# Sign the broker certificate with the CA
keytool -keystore keystore.jks -alias broker -certreq -file broker.csr -storepass password
keytool -keystore ca.keystore.jks -alias ca -gencert -infile broker.csr -outfile broker-ca.crt -storepass password -validity 3650
keytool -keystore keystore.jks -alias broker -importcert -file broker-ca.crt -storepass password -noprompt