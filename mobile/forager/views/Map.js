import { Button, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useRef, useState, useEffect} from 'react';
import MapView, { Callout, Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import * as FileSystem from 'expo-file-system';
import { shareAsync } from 'expo-sharing';
import * as Location from 'expo-location';




export default function Map({navigation}) {
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


  
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Map Screen</Text>
        <Button
        title="Go to Pin"
        onPress={() => navigation.navigate('Pin')}
      />
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
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  map: {
    width: '100%',
    height: '100%'
  }
});
