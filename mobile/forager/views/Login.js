import { Button, StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import backgroundImage from "../assets/british-library-eCm6i7V8EAs-unsplash.jpg"
export default function Login({navigation}) {
  return (
    <View style={styles.container}>
        <Text style={styles.title}>Forager</Text>
        <Image source ={backgroundImage} style={styles.image}></Image>
        
        
    <TouchableOpacity onPress={() => navigation.navigate('Map')} style={styles.appButtonContainer}>
		<Text style={styles.appButtonText}>Login</Text>
	</TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e3e1d5',
    alignItems: 'center',
    
  },

  title: {
    paddingTop: '15%',
    fontSize: '45%',
    fontFamily: 'Cochin'
    
  },
  image: {
    height: '30%',
    width: '85%',
    marginTop: '10%',
    marginBottom: '10%'
  },

  appButtonContainer: {
    elevation: 8,
    backgroundColor: "#808516",
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 12,
    width: '45%',
    alignSelf: 'center'
  },
  appButtonText: {
    fontSize: 18,
    color: "#fff",
    
    alignSelf: "center",
    
    
  },

});
