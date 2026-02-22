import { useMemo, useState } from 'react';

const OUTER_TABS = ['Data Input', 'Analysis & Result', 'Extra'];

const DATA_INPUT_TABS = [
  'Parameter Input',
  'Frequency Data',
  'Consequence Data',
  'Safety system & Human factor',
];

const ANALYSIS_TABS = [
  'Frequency Analysis',
  'Consequence Analysis',
  'Risk Assessment',
];

const groupRows = [
  { group: 'Group 1', phase: 'Gas', pressure: '18', temp: '24', size: '100' },
  { group: 'Group 2', phase: 'Liquid', pressure: '12', temp: '16', size: '50' },
  { group: 'Group 3', phase: 'Gas', pressure: '20', temp: '21', size: '125' },
];

const frequencyTable = [
  [
    '1',
    '1.234e-05',
    '8.920e-06',
    '2.331e-06',
    '5.010e-07',
    '2.900e-08',
    '2.397e-05',
  ],
  [
    '2',
    '9.540e-06',
    '7.310e-06',
    '2.102e-06',
    '4.300e-07',
    '2.310e-08',
    '1.942e-05',
  ],
  [
    'Total',
    '2.188e-05',
    '1.623e-05',
    '4.433e-06',
    '9.310e-07',
    '5.210e-08',
    '4.339e-05',
  ],
];

const consequenceRows = [
  ['1', 'Gas', '18', '24', '10-50mm', '2.001e-01', 'plume', '3.102e-02'],
  ['1', 'Gas', '18', '24', '50-150mm', '4.812e-01', 'plume', '5.233e-02'],
  ['2', 'Liquid', '12', '16', '10-50mm', '1.233e-01', 'puff', '2.114e-02'],
];

const consequenceFields = [
  ['Gas density (kg/m3)', '1.2'],
  ['Liquid density (kg/m3)', '800.0'],
  ['GOR (-)', '5.0'],
  ['Wind speed (m/s)', '3.0'],
  ['Release height (m)', '10.0'],
  ['Stability class', 'D'],
  ['Dispersion model', 'plume'],
  ['Max x (m)', '50.0'],
  ['y (m)', '0.0'],
  ['z (m)', '0.0'],
  ['Puff time (s)', '30.0'],
  ['Release duration (s)', '60.0'],
  ['Critical conc. (kg/m3)', '0.0'],
];

const explosionFields = [
  ['Eta (0.005 - 0.2)', '0.01'],
  ['Mass (kg)', '1.0'],
  ['Heat combustion (kJ/kg)', '0.0'],
  ['TNT heat (kJ/kg)', '4680.0'],
  ['Distance (m)', '10.0'],
  ['Ambient pressure p0 (bar)', '1.013'],
];

const poolFireFields = [
  ['Heat release rate Q (kW)', '1000.0'],
  ['Pool diameter D (m)', '5.0'],
  ['Distance x (m)', '20.0'],
  ['Radiative fraction f (0-1)', '0.35'],
  ['Transmissivity tau (0-1)', '1.0'],
];

function FieldGrid({ fields, compact = false }) {
  return (
    <div className={`field-grid ${compact ? 'field-grid--compact' : ''}`}>
      {fields.map(([label, value]) => (
        <label key={label}>
          <span>{label}</span>
          <input defaultValue={value} />
        </label>
      ))}
    </div>
  );
}

function SectionCard({ title, children, actions }) {
  return (
    <section className='section-card'>
      <div className='section-card__head'>
        <h3>{title}</h3>
        {actions ? (
          <div className='section-card__actions'>{actions}</div>
        ) : null}
      </div>
      {children}
    </section>
  );
}

function DataInputPanel({ tab }) {
  if (tab === 'Parameter Input') {
    return (
      <SectionCard title='Parameter Input'>
        <p className='placeholder-copy'>
          Parameter Input area mirrored from Tkinter layout.
        </p>
      </SectionCard>
    );
  }

  if (tab === 'Safety system & Human factor') {
    return (
      <SectionCard title='Safety system & Human factor'>
        <p className='placeholder-copy'>
          Safety system & Human factor area mirrored from Tkinter layout.
        </p>
      </SectionCard>
    );
  }

  if (tab === 'Consequence Data') {
    return (
      <div className='stack-grid'>
        <SectionCard title='Consequence Inputs'>
          <FieldGrid fields={consequenceFields} />
        </SectionCard>
        <SectionCard title='Explosion Model Inputs (TNT / TNO / BST)'>
          <FieldGrid fields={explosionFields} compact />
        </SectionCard>
        <SectionCard
          title='Pool Fire Model Inputs'
          actions={<button className='btn btn--primary'>Save Inputs</button>}
        >
          <FieldGrid fields={poolFireFields} compact />
        </SectionCard>
      </div>
    );
  }

  return (
    <div className='frequency-layout'>
      <div className='frequency-layout__main'>
        <SectionCard title='Grouping'>
          <div className='split-panels'>
            <div className='mini-panel'>
              <h4>Group Controls</h4>
              <label>
                <span>Operation hours (/year)</span>
                <input defaultValue='0' />
              </label>
              <div className='button-row'>
                <button className='btn btn--info'>Save</button>
                <button className='btn btn--danger'>Reset</button>
              </div>
            </div>

            <div className='mini-panel'>
              <h4>View of All Groups</h4>
              <table>
                <thead>
                  <tr>
                    <th>Group</th>
                    <th>Phase</th>
                    <th>Working Press. (bar)</th>
                    <th>Working Temp. (°C)</th>
                    <th>System Size (mm)</th>
                  </tr>
                </thead>
                <tbody>
                  {groupRows.map((row) => (
                    <tr key={row.group}>
                      <td>{row.group}</td>
                      <td>{row.phase}</td>
                      <td>{row.pressure}</td>
                      <td>{row.temp}</td>
                      <td>{row.size}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </SectionCard>

        <div className='split-panels split-panels--aligned'>
          <SectionCard title='Operational Conditions'>
            <div className='field-grid field-grid--compact'>
              <label>
                <span>Fuel Phase</span>
                <select defaultValue='Gas'>
                  <option>Liquid</option>
                  <option>Gas</option>
                </select>
              </label>
              <label>
                <span>Pressure (Bar)</span>
                <input defaultValue='10' />
              </label>
              <label>
                <span>Temperature (°C)</span>
                <input defaultValue='20' />
              </label>
              <label>
                <span>Size (mm)</span>
                <input defaultValue='50' />
              </label>
            </div>
            <button className='btn btn--success'>OK</button>
          </SectionCard>

          <SectionCard title='Add Group'>
            <div className='add-group-actions'>
              <button className='btn btn--info'>New Group</button>
              <button className='btn btn--primary'>Save Groups</button>
              <button className='btn btn--danger'>STOP</button>
              <button className='btn btn--success'>Generate Analysis</button>
            </div>
          </SectionCard>
        </div>

        <SectionCard title='Equipment List-Up'>
          <div className='field-grid field-grid--compact'>
            <label>
              <span>Name of Equipment</span>
              <select defaultValue='10. Process Pipe'>
                <option>1. Centrifugal Compressor</option>
                <option>10. Process Pipe</option>
                <option>11. Centrifugal Pump</option>
                <option>16. Process Vessel</option>
              </select>
            </label>
            <label>
              <span>Size</span>
              <select defaultValue='100mm'>
                <option>50mm</option>
                <option>100mm</option>
                <option>125mm</option>
              </select>
            </label>
            <label>
              <span>EA</span>
              <input defaultValue='1' />
            </label>
          </div>
          <div className='button-row'>
            <button className='btn btn--success'>Add ✓</button>
            <button className='btn btn--info'>Remove −</button>
          </div>
        </SectionCard>

        <SectionCard title='Group Specifics'>
          <div className='section-inline-control'>
            <label>
              <span>Select Group Number</span>
              <input defaultValue='1' />
            </label>
          </div>
          <table>
            <thead>
              <tr>
                <th>No.</th>
                <th>Equip. List</th>
                <th>Size</th>
                <th>EA</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>10. Process Pipe</td>
                <td>100mm</td>
                <td>2</td>
              </tr>
              <tr>
                <td>2</td>
                <td>11. Centrifugal Pump</td>
                <td>50mm</td>
                <td>1</td>
              </tr>
            </tbody>
          </table>
        </SectionCard>
      </div>
    </div>
  );
}

function AnalysisPanel({ tab }) {
  if (tab === 'Risk Assessment') {
    return (
      <SectionCard title='Risk Assessment'>
        <p className='placeholder-copy'>
          Risk Assessment area mirrored from Tkinter layout.
        </p>
      </SectionCard>
    );
  }

  if (tab === 'Consequence Analysis') {
    return (
      <div className='stack-grid'>
        <SectionCard title='Consequence Analysis Header'>
          <p className='summary-line'>
            Inputs: gas rho=1.20 kg/m3, liq rho=800.0 kg/m3, GOR=5.00, u=3.0
            m/s, H=10.0 m, stability=D, model=plume, x_max/y/z=(50.0,0.0,0.0)
          </p>
        </SectionCard>

        <SectionCard title='Explosion / Pool Fire Outputs'>
          <dl className='metrics-list'>
            <div>
              <dt>TNT equivalent mass W (kg)</dt>
              <dd>0.002</dd>
            </div>
            <div>
              <dt>Scaled distance Z_e (-)</dt>
              <dd>79.370</dd>
            </div>
            <div>
              <dt>Overpressure P_s (bar)</dt>
              <dd>0.002</dd>
            </div>
            <div>
              <dt>TNO overpressure P_s (bar)</dt>
              <dd>-</dd>
            </div>
            <div>
              <dt>BST overpressure P_s (bar)</dt>
              <dd>-</dd>
            </div>
            <div>
              <dt>Pool fire radiant flux q'' (kW/m2)</dt>
              <dd>1.114</dd>
            </div>
          </dl>
        </SectionCard>

        <SectionCard
          title='Consequence Result Table'
          actions={
            <div className='button-row button-row--tight'>
              <button className='btn btn--primary'>
                Run Consequence Analysis
              </button>
              <button className='btn btn--neutral'>Reload Inputs</button>
            </div>
          }
        >
          <table>
            <thead>
              <tr>
                <th>Group</th>
                <th>Phase</th>
                <th>Pressure (bar)</th>
                <th>Temp</th>
                <th>Leak Cat</th>
                <th>Leak Rate (kg/s)</th>
                <th>Dispersion</th>
                <th>C (kg/m3)</th>
              </tr>
            </thead>
            <tbody>
              {consequenceRows.map((row, idx) => (
                <tr key={`${row[0]}-${idx}`}>
                  {row.map((cell, i) => (
                    <td key={`${idx}-${i}`}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <div className='button-row'>
            <button className='btn btn--neutral'>Plot Dispersion (3D)</button>
            <button className='btn btn--neutral'>Plot Dispersion (2D)</button>
            <button className='btn btn--neutral'>Plot Explosion (TNT)</button>
            <button className='btn btn--neutral'>Plot Explosion (TNO)</button>
            <button className='btn btn--neutral'>Plot Explosion (BST)</button>
            <button className='btn btn--neutral'>Plot Pool Fire</button>
          </div>
        </SectionCard>
      </div>
    );
  }

  return (
    <div className='analysis-layout'>
      <SectionCard title='Frequency Analysis Graph'>
        <div className='graph-placeholder'>
          <div className='graph-placeholder__line' />
          <p>Leak Freq. (/year) vs Leak Size (mm)</p>
        </div>
      </SectionCard>

      <SectionCard title='Sub Groups'>
        <ul className='legend-list'>
          <li>
            <span className='dot dot--a' /> Group 1
          </li>
          <li>
            <span className='dot dot--b' /> Group 2
          </li>
          <li>
            <span className='dot dot--c' /> Group 3
          </li>
        </ul>
      </SectionCard>

      <SectionCard title='Frequency Data Table'>
        <table>
          <thead>
            <tr>
              <th>Group</th>
              <th>1-3mm</th>
              <th>3-10mm</th>
              <th>10-50mm</th>
              <th>50-150mm</th>
              <th>&gt;150mm</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            {frequencyTable.map((row, idx) => (
              <tr
                key={`${row[0]}-${idx}`}
                className={row[0] === 'Total' ? 'row-total' : ''}
              >
                {row.map((cell, i) => (
                  <td key={`${idx}-${i}`}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </SectionCard>
    </div>
  );
}

function InnerTabs({ tabs, selected, onChange }) {
  return (
    <nav className='inner-tabs' aria-label='section tabs'>
      {tabs.map((tab) => (
        <button
          key={tab}
          className={`inner-tab ${selected === tab ? 'is-active' : ''}`}
          onClick={() => onChange(tab)}
          type='button'
        >
          {tab}
        </button>
      ))}
    </nav>
  );
}

export default function App() {
  const [outerTab, setOuterTab] = useState('Data Input');
  const [dataTab, setDataTab] = useState('Frequency Data');
  const [analysisTab, setAnalysisTab] = useState('Frequency Analysis');
  const [theme, setTheme] = useState('light');

  const pageClass = useMemo(() => `app-shell theme-${theme}`, [theme]);

  return (
    <div className={pageClass}>
      <header className='topbar'>
        <div>
          <h1>Maritime Alternative Fuel Risk Assessment</h1>
        </div>
        <button
          className='btn btn--neutral'
          onClick={() => setTheme((v) => (v === 'light' ? 'dark' : 'light'))}
          type='button'
        >
          {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
        </button>
      </header>

      <div className='workspace'>
        <aside className='outer-tabs' aria-label='main sections'>
          {OUTER_TABS.map((tab) => (
            <button
              key={tab}
              className={`outer-tab ${outerTab === tab ? 'is-active' : ''}`}
              onClick={() => setOuterTab(tab)}
              type='button'
            >
              {tab}
            </button>
          ))}
        </aside>

        <main className='content-panel'>
          {outerTab === 'Data Input' ? (
            <>
              <InnerTabs
                tabs={DATA_INPUT_TABS}
                selected={dataTab}
                onChange={setDataTab}
              />
              <DataInputPanel tab={dataTab} />
            </>
          ) : null}

          {outerTab === 'Analysis & Result' ? (
            <>
              <InnerTabs
                tabs={ANALYSIS_TABS}
                selected={analysisTab}
                onChange={setAnalysisTab}
              />
              <AnalysisPanel tab={analysisTab} />
            </>
          ) : null}

          {outerTab === 'Extra' ? (
            <SectionCard title='Extra'>
              <p className='placeholder-copy'>
                Extra tools section mirrored from Tkinter placeholder tab.
              </p>
            </SectionCard>
          ) : null}
        </main>
      </div>
    </div>
  );
}
