import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Image, Button,TextInput, TouchableOpacity} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import base64 from 'react-native-base64'
import leaf from '../assets/leaf.png'
export default function Add({navigation}) {
	const [image, setImage] = useState(null);
	const [base64Image, setBase64Image] = useState(null);
	const [note, setNote] = useState(null);
	const [location, setLocation] = useState("test");
	const [isToxic, setisToxic] = useState(0);
	const [name, setName] = useState("test");
	
	const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({  
			
								imageURL: {image},
								name: "name",
								isEdible: true,
								location: "test location",
								note: "test",
								
							})
    };
  
    const postPin = async () => {
        try {
            await fetch(
                'https://128.180.239.157:8000/addpin', requestOptions)
                .then(response => {
                    response.json()
                        .then(data => {
							console.log("")
                            Alert.alert("Post created at : ", 
                            data.createdAt);
                        });
                })
        }
        catch (error) {
            console.error(error);
        }
    }

  const pickImage = async () => {
	
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    console.log(result);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
	  //setBase64Image(base64.encode(result.assets[0].uri))
    }
  };
		
		  return (
			<View style={styles.container}>
				
				<TouchableOpacity onPress={pickImage} style={styles.appButtonContainer}>
					<Text style={styles.appButtonText}>Add Image</Text>
				</TouchableOpacity>
				{image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
				<Text style={styles.text}>Add Note: </Text>
				<TextInput
					style={styles.input}
					onChangeText={setNote}
					value={note}
					placeholder='enter text here'
				/> 
				
				<TouchableOpacity onPress={postPin} style={styles.appButtonContainer}>
					<Text style={styles.appButtonText}>Post</Text>
				</TouchableOpacity>
				<Image source={leaf} style={styles.leaf}></Image>
			</View>
		  );
		
	  }
	  const styles = StyleSheet.create({
		container: {
		  flex: 1,
		  padding: 30,
		  paddingTop: '20%',
		//   alignItems: 'center',
		//   justifyContent: 'center',
		  backgroundColor: '#e3e1d5'
		},
		button: {
		  width: 250,
		  height: 60,
		  backgroundColor: '#3740ff',
		  alignItems: 'center',
		  justifyContent: 'center',
		  borderRadius: 4,
		  marginBottom:12    
		},
		buttonText: {
		  textAlign: 'center',
		  fontSize: 15,
		  color: '#fff'
		},
		input: {
			height: 40,
			margin: 12,
			borderWidth: 1,
			padding: 10,
			
		  },
		  leaf: {
			position: 'absolute',
			height: '40%',
			width: '80%',
		    left: 0,
			bottom: 0,
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

		  text: {
			textAlign: 'center',
			fontSize: 18,
			paddingTop: '10%',
			fontWeight: 'bold',
			color: "#808516"
		  },

		  
	  });