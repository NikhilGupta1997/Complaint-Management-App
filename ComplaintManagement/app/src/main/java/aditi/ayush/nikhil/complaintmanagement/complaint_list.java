package aditi.ayush.nikhil.complaintmanagement;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ExpandableListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class complaint_list extends Fragment
    {/** A class for the Grades Tab **/
        ExpandableListAdapter listAdapter;
        public static ExpandableListView expListView;
        public static List<String> listDataHeader;
        HashMap<String, List<String>> listDataChild;
        MyApp_cookie app_list=new MyApp_cookie();
        private long mRequestStartTime;



        public complaint_list() {
        // Required empty public constructor
    }

        @Override
        public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        }
    private void prepareListData()
    {/** A method to populate the Expandable List view for the Grades Tab"**/
        final int[] no_assign = {0};
        final JSONArray noti =new JSONArray();
        listDataHeader = new ArrayList<String>();
        listDataChild = new HashMap<String, List<String>>();
        mRequestStartTime = System.currentTimeMillis();
        String url1="http://10.192.38.23:8000/complaint_data/get_all.json";
        String url="http://10.192.38.23:8000/default/logout.json";
        Log.i("yo", " Fetching JSON");
        StringRequest json_ob = new StringRequest (Request.Method.GET, url1,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response)
                    {
                        Log.i("yo", "why this ... working" + response);
///                        System.out.println(response.toString());
                        Toast.makeText(getActivity().getApplicationContext(),
                                "Logout ",
                                Toast.LENGTH_LONG).show();
                        try
                        {
                            JSONObject json_data = new JSONObject(response);

                            String data1 = json_data.getString("Institute");
                            String data2 = json_data.getString("Hostel");
                            String data3 = json_data.getString("Individual");

                            JSONArray inst = new JSONArray(data1);
                            JSONArray host = new JSONArray(data2);
                            JSONArray indv = new JSONArray(data3);

                            int i=0;

                            listDataHeader.add("Individual");//course code + Assignment naINme
                            List<String> expand1 = new ArrayList<String>();
                            no_assign[0] =inst.length();
                            for(;i<no_assign[0];i++)
                            {   JSONObject notification =inst.getJSONObject(i);
                                String content = notification.getString("complaint_content");


                                expand1.add(content);

                            }
                            listDataChild.put("Individual", expand1);

                            listDataHeader.add("Individual");//course code + Assignment naINme
                            List<String> expand2 = new ArrayList<String>();
                            no_assign[0] =host.length();
                            for(;i<no_assign[0];i++)
                            {   JSONObject notification =host.getJSONObject(i);
                                String content = notification.getString("complaint_content");


                                expand2.add(content);

                            }
                            listDataChild.put("Individual", expand2);

                            listDataHeader.add("Individual");//course code + Assignment naINme
                            List<String> expand3 = new ArrayList<String>();
                            no_assign[0] =indv.length();
                            for(;i<no_assign[0];i++)
                            {   JSONObject notification =indv.getJSONObject(i);
                                String content = notification.getString("complaint_content");


                                expand3.add(content);

                            }
                            listDataChild.put("Individual", expand3);

                            long totalRequestTime = System.currentTimeMillis() - mRequestStartTime;
                            System.out.println("Response time for one is=="+ totalRequestTime );






                        } catch (Exception e)
                        {
                            e.printStackTrace();
                            Toast.makeText(getActivity().getApplicationContext(),
                                    "Error: " + e.getMessage(),
                                    Toast.LENGTH_LONG).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i("yo", "why this not working");
                        //  Toast.makeText(getActivity().getApplicationContext(), error.toString(), Toast.LENGTH_LONG).show();
                    }
                });
        Volley.newRequestQueue(getActivity().getApplicationContext()).add(json_ob);
        try {
            Thread.sleep(1000);                 //1000 milliseconds is one second.
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }


        System.out.println("yo:"+listDataChild.size());
        System.out.println(listDataHeader.size());
//        listDataChild.put(listDataHeader.get(0), top250); // Header, Child data
//        listDataChild.put(listDataHeader.get(1), nowShowing);
//        listDataChild.put(listDataHeader.get(2), comingSoon);
//
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
/** Inflate the layout for grades tab **/
        View rootView = inflater.inflate(R.layout.fragment_complaint_list, null);

        expListView = (ExpandableListView) rootView.findViewById(R.id.cmpExp);

        prepareListData();

        listAdapter = new ExpandableListAdapter(getActivity(), listDataHeader, listDataChild);
        expListView.setAdapter(listAdapter);

        Log.i("groups", listDataHeader.toString());
        Log.i("details", listDataChild.toString());

        // Listview Group click listener
        expListView.setOnGroupClickListener(new ExpandableListView.OnGroupClickListener() {

            @Override
            public boolean onGroupClick(ExpandableListView parent, View v, int groupPosition, long id) {
                // Toast.makeText(getApplicationContext(),
                // "Group Clicked " + listDataHeader.get(groupPosition),
                // Toast.LENGTH_SHORT).show();
                return false;
            }
        });

        // Listview Group expanded listener
        expListView.setOnGroupExpandListener(new ExpandableListView.OnGroupExpandListener() {

            @Override
            public void onGroupExpand(int groupPosition)
            {
                //    Toast.makeText(getActivity().getApplicationContext(), listDataHeader.get(groupPosition) + " Expanded", Toast.LENGTH_SHORT).show();
            }
        });

        // Listview Group collasped listener
        expListView.setOnGroupCollapseListener(new ExpandableListView.OnGroupCollapseListener() {

            @Override
            public void onGroupCollapse(int groupPosition)
            {
                //    Toast.makeText(getActivity().getApplicationContext(), listDataHeader.get(groupPosition) + " Collapsed", Toast.LENGTH_SHORT).show();
            }
        });

        // Listview on child click listener
        expListView.setOnChildClickListener(new ExpandableListView.OnChildClickListener()
        {
            @Override
            public boolean onChildClick(ExpandableListView parent, View v,
                                        int groupPosition, int childPosition, long id) {
                //        Toast.makeText(getActivity().getApplicationContext(), listDataHeader.get(groupPosition) + " : " + listDataChild.get(listDataHeader.get(groupPosition)).get(childPosition), Toast.LENGTH_SHORT).show();
                return false;
            }
        });
        return rootView;
    }


}