/**
 * Represents trip data.
 */
export interface Trip {
  /**
   * The unique identifier for the trip.
   */
  _id: { $oid: string };
  unique_id: number;
  invoice_number: string;
  source_address: string;
  destination_address: string;
  sourceLocation: number[];
  destinationLocation: number[];
  payment_mode: number;
  total_distance: number;
  total_time: number;
  payment_status: number;
  is_trip_end: number;
  is_trip_completed: number;
  payment_mode: number;
  payment_status: number;
  accepted_time: { $date: string };
  created_at: { $date: string };
}

import { MongoClient, ServerApiVersion } from 'mongodb';

// Connection URI
const uri = process.env.MONGODB_URI;

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri!, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

/**
 * Asynchronously retrieves trip data from MongoDB.
 * @returns A promise that resolves to an array of Trip objects.
 */
export async function getTrips(): Promise<Trip[]> {
  try {
    // Connect the client to the server	(optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");

    const db = client.db('CabE'); // Replace with your actual database name
    const tripsCollection = db.collection<Trip>('trip_histories'); // Replace with your actual collection name
    const trips = await tripsCollection.find().toArray();

    return trips;
  } catch(e) {
    console.error(e);
    return [];
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
