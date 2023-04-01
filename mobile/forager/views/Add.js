import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Image, Button,TextInput} from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function Add({navigation}) {
	const [image, setImage] = useState(null);
	const [note, setNote] = useState(null);
	const [location, setLocation] = useState(null);


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
    }
  };
		
		  return (
			<View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
				<Button title="Pick an image from camera roll" onPress={pickImage} />
				{image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
				<Text>Add Note: </Text>
				<TextInput
					style={styles.input}
					onChangeText={setNote}
					value={note}
					placeholder='enter a note here'
				/> 
			</View>
		  );
		
	  }
	  const styles = StyleSheet.create({
		container: {
		  flex: 1,
		  padding: 30,
		  alignItems: 'center',
		  justifyContent: 'center',
		  backgroundColor: '#fff'
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
	  });