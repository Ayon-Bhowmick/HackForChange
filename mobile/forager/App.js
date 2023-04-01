import React from 'react';
import { StyleSheet, View } from 'react-native';
import MapView, {PROVIDER_GOOGLE} from 'react-native-maps';


export default function App() {
  return (
    <View style={styles.container}>
      <MapView style={styles.map} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
});