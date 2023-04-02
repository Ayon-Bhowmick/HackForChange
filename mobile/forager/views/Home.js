import { supabase } from '../services/supabase';
import { Button, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useRef, useState, useEffect} from 'react';
import MapView, { Callout, Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import * as FileSystem from 'expo-file-system';
import { shareAsync } from 'expo-sharing';
import * as Location from 'expo-location';


export function Home({navigation}) {
    Location.setGoogleApiKey("AIzaSyAwDCdf88Yq2ZroapxOY-FyfxEvBN0Ymx8");

    const [location, setLocation] = useState();

    useEffect(() => {
        const getPermissions = async () => {
          let { status } = await Location.requestForegroundPermissionsAsync();
          if (status !== 'granted'){
            console.log("Please grant location permissions");
            return;
          }
    
          let currentLocation = await Location.getCurrentPositionAsync({});
          setLocation(currentLocation);
          console.log("Location:");
          console.log(currentLocation);
        };
        getPermissions();
      },[]);
      const onRegionChange = (region) => {
        {/* console.log(region); */}
      };

    const [user, setUser] = useState({
        name: "Loading...",
        email: "Loading...",
        phone: "Loading..."
    })

    const signout = async () => {
        const { error } = await supabase.auth.signOut()
        if(error) return console.log(error)
    }

    useEffect(() => {
        supabase.auth.getSession()
        .then(({ data, error }) => {
            const { phone, user_metadata } = data.session.user
            const { full_name: name, email } = user_metadata
            setUser({name, email, phone}) 
        })
    }, [])

    return (
        <View>
            <Text>Name: {user.name}</Text>
            <Text>Email: {user.email}</Text>
            {/*<Button title='Sign Out' onPress={() => signout()}/>*/}
        <TouchableOpacity onPress={() => navigation.navigate('Add')} style={styles.appButtonContainer}>
          <Text style={styles.appButtonText}>+</Text>
        </TouchableOpacity>
        <MapView 
          style={styles.map}
          onRegionChange={onRegionChange}
          initialRegion={
            {"latitude": -28.01314062143307,
             "latitudeDelta": 117.83619225304881,
             "longitude": 122.59707705899388,
             "longitudeDelta": 85.80645666457133}
          }
          
          >
          </MapView>
       </View>
    )
}

const styles = StyleSheet.create({
    container: {
      // flex: 1,
       backgroundColor: '#e3e1d5',
      // alignItems: 'top',
      // justifyContent: 'center',
    },
    map: {
      width: '100%',
      height: '100%',
      top: 0
      
    },
  
    button: {
      position: 'absolute',
      top: 30,
      
  
    },
  
    appButtonContainer: {
      elevation: 8,
      backgroundColor: "#808516",
      borderRadius: 100,
      paddingVertical: 10,
      paddingHorizontal: 12,
      width: 62,
      alignSelf: 'center',
      position: 'absolute',
      bottom: '7%',
      zIndex: 5,
    },
    appButtonText: {
      fontSize: 35,
      color: "#fff",
      
      alignSelf: "center",
      
      
    },
  });